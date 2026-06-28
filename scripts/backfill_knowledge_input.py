"""
backfill_knowledge_input.py
───────────────────────────
One-shot migration script: copies artefacts from every existing
dataset/crawled/<domain>/ folder into the correct knowledge_input/
category subfolder so that the "Arquivos Monitorados" tab is populated
with all previously crawled sites.

Mapping:
  screenshot.png  → knowledge_input/images/<domain>/screenshot.png
  page.html       → knowledge_input/references/<domain>/page.html
  style.css       → knowledge_input/design_systems/<domain>/style.css
  (creates)       → knowledge_input/references/<domain>/metadata.txt

Usage:
  python scripts/backfill_knowledge_input.py
"""

import os
import shutil
import sys

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRAWLED_DIR = os.path.join(BASE_DIR, "dataset", "crawled")
KNOWLEDGE_INPUT_DIR = os.path.join(BASE_DIR, "knowledge_input")

# ── Extension-to-category mapping ────────────────────────────────────────────
EXT_TO_CATEGORY = {
    ".png":  "images",
    ".jpg":  "images",
    ".jpeg": "images",
    ".webp": "images",
    ".html": "references",
    ".htm":  "references",
    ".css":  "design_systems",
    ".txt":  "references",
}


def backfill() -> None:
    if not os.path.isdir(CRAWLED_DIR):
        print(f"[ERROR] Crawled directory not found: {CRAWLED_DIR}")
        sys.exit(1)

    domains = [
        d for d in os.listdir(CRAWLED_DIR)
        if os.path.isdir(os.path.join(CRAWLED_DIR, d))
    ]

    if not domains:
        print("[INFO] No crawled domains found. Nothing to backfill.")
        return

    print(f"[INFO] Found {len(domains)} domain folders to backfill.\n")

    total_copied = 0
    total_skipped = 0

    for domain in sorted(domains):
        domain_dir = os.path.join(CRAWLED_DIR, domain)
        files = [f for f in os.listdir(domain_dir) if os.path.isfile(os.path.join(domain_dir, f))]

        for filename in files:
            src_path = os.path.join(domain_dir, filename)

            _, ext = os.path.splitext(filename.lower())
            category = EXT_TO_CATEGORY.get(ext)
            if not category:
                continue  # skip unknown types

            dest_dir = os.path.join(KNOWLEDGE_INPUT_DIR, category, domain)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, filename)

            if os.path.exists(dest_path):
                total_skipped += 1
                continue  # already exported

            shutil.copy2(src_path, dest_path)
            total_copied += 1
            print(f"  [COPY] {category}/{domain}/{filename}")

        # Always create a metadata.txt reference stub for every domain
        meta_dir = os.path.join(KNOWLEDGE_INPUT_DIR, "references", domain)
        os.makedirs(meta_dir, exist_ok=True)
        meta_path = os.path.join(meta_dir, "metadata.txt")
        if not os.path.exists(meta_path):
            with open(meta_path, "w", encoding="utf-8") as f:
                f.write(f"Domain: {domain}\n")
                f.write(f"Source: dataset/crawled/{domain}\n")
                f.write(f"Files: {', '.join(files)}\n")
            total_copied += 1
            print(f"  [META] references/{domain}/metadata.txt")

    print(f"\n[DONE] Backfill complete.")
    print(f"       Copied : {total_copied} files")
    print(f"       Skipped: {total_skipped} (already existed)")


if __name__ == "__main__":
    backfill()
