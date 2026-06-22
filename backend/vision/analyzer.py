import os
from typing import Dict, List, Tuple
from PIL import Image
from backend.schemas.vision import ColorPalette, GridLayout, SpacingMetrics, VisualDensity, VisionMetadata
from backend.utils.custom_logger import setup_logger

logger = setup_logger("vision.analyzer")


class VisionAnalyzer:
    """Service to perform visual analysis on crawled page screenshots

    using Pillow (PIL) for image-based heuristics.
    """

    def analyze(self, image_path: str) -> VisionMetadata:
        logger.info(f"Starting visual analysis on: {image_path}")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Screenshot image not found at: {image_path}")

        try:
            with Image.open(image_path) as img:
                orig_width, orig_height = img.size
                logger.debug(f"Loaded image size: {orig_width}x{orig_height}")

                # 1. Downscale image for fast pixel operations (maintaining aspect ratio)
                process_width = 150
                scale_factor = process_width / orig_width
                process_height = int(orig_height * scale_factor)
                
                # Use Resampling.LANCZOS (standard in Pillow)
                resized_img = img.convert("RGB").resize(
                    (process_width, process_height), Image.Resampling.LANCZOS
                )
                logger.debug(f"Resized image for analysis: {process_width}x{process_height}")

                # Retrieve all pixels
                pixels = list(resized_img.getdata())

                # 2. Extract Color Palette
                colors_data = self._extract_colors(pixels)
                dominant_colors = colors_data["dominant_colors"]
                bg_color_rgb = colors_data["bg_color_rgb"]
                bg_color_hex = colors_data["bg_color_hex"]

                # 3. Analyze Visual Density
                density = self._calculate_density(pixels, bg_color_rgb)

                # 4. Analyze Margins & Spacing
                spacing = self._calculate_spacing(resized_img, bg_color_rgb, scale_factor)

                # 5. Analyze Layout Grid Splits
                grid = self._calculate_grid(resized_img, bg_color_rgb)

                logger.info("Visual analysis completed successfully.")
                return VisionMetadata(
                    colors=ColorPalette(
                        dominant_colors=dominant_colors,
                        background_color=bg_color_hex,
                    ),
                    grid=grid,
                    spacing=spacing,
                    density=density,
                )

        except Exception as e:
            logger.exception(f"Error analyzing image {image_path}: {e}")
            raise

    def _extract_colors(self, pixels: List[Tuple[int, int, int]]) -> Dict:
        """Groups colors into discrete buckets to locate dominant shades."""
        bucket_counts = {}
        for r, g, b in pixels:
            # Bucket colors to nearest multiple of 16 to group similar shades
            bucket = (r // 16 * 16, g // 16 * 16, b // 16 * 16)
            bucket_counts[bucket] = bucket_counts.get(bucket, 0) + 1

        # Sort buckets by frequency
        sorted_buckets = sorted(bucket_counts.items(), key=lambda item: item[1], reverse=True)

        dominant_hex = []
        bg_rgb = (255, 255, 255)  # fallback
        bg_hex = "#ffffff"

        for i, (rgb, count) in enumerate(sorted_buckets[:5]):
            hex_code = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
            dominant_hex.append(hex_code)
            if i == 0:
                bg_rgb = rgb
                bg_hex = hex_code

        return {
            "dominant_colors": dominant_hex,
            "bg_color_rgb": bg_rgb,
            "bg_color_hex": bg_hex,
        }

    def _rgb_distance(self, c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> float:
        """Calculates Euclidean distance between two RGB colors."""
        return ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2) ** 0.5

    def _calculate_density(
        self, pixels: List[Tuple[int, int, int]], bg_rgb: Tuple[int, int, int]
    ) -> VisualDensity:
        """Determines ratio of active content pixels vs empty background area."""
        total_pixels = len(pixels)
        if total_pixels == 0:
            return VisualDensity(content_percentage=0.0, whitespace_percentage=100.0)

        # Count pixels that significantly differ from background color
        content_pixels = 0
        threshold = 30.0  # Euclidean color distance threshold
        for p in pixels:
            if self._rgb_distance(p, bg_rgb) > threshold:
                content_pixels += 1

        content_percent = round((content_pixels / total_pixels) * 100.0, 2)
        whitespace_percent = round(100.0 - content_percent, 2)

        return VisualDensity(
            content_percentage=content_percent,
            whitespace_percentage=whitespace_percent,
        )

    def _calculate_spacing(
        self, img: Image.Image, bg_rgb: Tuple[int, int, int], scale_factor: float
    ) -> SpacingMetrics:
        """Estimates page margins by detecting consistent background blocks from edges."""
        width, height = img.size
        threshold = 25.0

        # Helper to check if a row is mostly background
        def is_row_bg(y: int) -> bool:
            bg_pixels = 0
            for x in range(width):
                if self._rgb_distance(img.getpixel((x, y)), bg_rgb) <= threshold:
                    bg_pixels += 1
            return (bg_pixels / width) >= 0.95

        # Helper to check if a column is mostly background
        def is_col_bg(x: int) -> bool:
            bg_pixels = 0
            for y in range(height):
                if self._rgb_distance(img.getpixel((x, y)), bg_rgb) <= threshold:
                    bg_pixels += 1
            return (bg_pixels / height) >= 0.95

        # Scan margins (resized scale)
        top_margin = 0
        while top_margin < height and is_row_bg(top_margin):
            top_margin += 1

        bottom_margin = 0
        while bottom_margin < height and is_row_bg(height - 1 - bottom_margin):
            bottom_margin += 1

        left_margin = 0
        while left_margin < width and is_col_bg(left_margin):
            left_margin += 1

        right_margin = 0
        while right_margin < width and is_col_bg(width - 1 - right_margin):
            right_margin += 1

        # Scale margins back to original resolution
        orig_top = int(top_margin / scale_factor)
        orig_bottom = int(bottom_margin / scale_factor)
        orig_left = int(left_margin / scale_factor)
        orig_right = int(right_margin / scale_factor)

        # Estimate content gaps (vertical empty space slices between content)
        content_gaps = []
        current_gap = 0
        # Start checking after top margin, end before bottom margin
        for y in range(top_margin, height - bottom_margin):
            if is_row_bg(y):
                current_gap += 1
            else:
                if current_gap > 1:  # ignore single pixel lines
                    content_gaps.append(int(current_gap / scale_factor))
                current_gap = 0

        # Unique, sorted list of spacing gaps
        unique_gaps = sorted(list(set(content_gaps)))

        return SpacingMetrics(
            margins={
                "top": orig_top,
                "bottom": orig_bottom,
                "left": orig_left,
                "right": orig_right,
            },
            content_gaps=unique_gaps[:5],  # top 5 key gaps
        )

    def _calculate_grid(self, img: Image.Image, bg_rgb: Tuple[int, int, int]) -> GridLayout:
        """Finds horizontal and vertical layout partitions (lines of clean background)."""
        width, height = img.size
        threshold = 25.0

        # Detect columns of background
        col_bg_status = []
        for x in range(width):
            bg_pixels = sum(
                1 for y in range(height)
                if self._rgb_distance(img.getpixel((x, y)), bg_rgb) <= threshold
            )
            col_bg_status.append((bg_pixels / height) >= 0.98)

        # Detect rows of background
        row_bg_status = []
        for y in range(height):
            bg_pixels = sum(
                1 for x in range(width)
                if self._rgb_distance(img.getpixel((x, y)), bg_rgb) <= threshold
            )
            row_bg_status.append((bg_pixels / width) >= 0.98)

        # Helper to group consecutive indices
        def find_split_midpoints(status_list: List[bool]) -> List[float]:
            midpoints = []
            in_split = False
            split_start = 0
            for idx, is_bg in enumerate(status_list):
                if is_bg and not in_split:
                    in_split = True
                    split_start = idx
                elif not is_bg and in_split:
                    in_split = False
                    # Middle of the split
                    midpoint = (split_start + idx - 1) / 2.0
                    # Relative position
                    midpoints.append(round(midpoint / len(status_list), 3))
            
            if in_split:
                midpoint = (split_start + len(status_list) - 1) / 2.0
                midpoints.append(round(midpoint / len(status_list), 3))
            return midpoints

        v_splits = find_split_midpoints(col_bg_status)
        h_splits = find_split_midpoints(row_bg_status)

        # Classify grid type based on splits
        # If there are horizontal columns (vertical splits) in the body area, it's a grid or columns
        # Filter out splits at the very edge (margins)
        active_v_splits = [s for s in v_splits if 0.15 < s < 0.85]
        active_h_splits = [s for s in h_splits if 0.15 < s < 0.85]

        if len(active_v_splits) >= 1 and len(active_h_splits) >= 1:
            grid_type = "grid"
        elif len(active_v_splits) >= 1:
            grid_type = f"multi_column_{len(active_v_splits) + 1}"
        elif len(active_h_splits) >= 2:
            grid_type = "stacked_sections"
        else:
            grid_type = "single_column"

        return GridLayout(
            vertical_splits=v_splits,
            horizontal_splits=h_splits,
            grid_type=grid_type,
        )
