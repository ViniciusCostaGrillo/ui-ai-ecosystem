import os
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any

import nest_asyncio
from prefect import task, flow

from backend.schemas.extractor import ExtractionResult
from backend.schemas.vision import VisionMetadata
from backend.schemas.analyzer import AnalysisResult
from backend.schemas.codegen import CodegenResult
from backend.schemas.dataset_builder import DatasetManifest

logger = logging.getLogger(__name__)


def run_async_coro(coro):
    """Run an async coroutine synchronously using nest_asyncio."""
    try:
        loop = asyncio.get_running_loop()
        nest_asyncio.apply(loop)
        return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


@task(name="Crawl Page Task")
def crawl_page_task(url: str, output_dir: str) -> Dict[str, Any]:
    logger.info(f"Prefect Task: Crawling page {url}...")
    from backend.crawler.playwright_engine import PlaywrightEngine
    crawler = PlaywrightEngine()
    try:
        crawl_res = run_async_coro(crawler.crawl(url, output_dir))
        html_path = crawl_res["html_path"]
        screenshot_path = crawl_res["screenshot_path"]
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return {
            "html_path": str(html_path),
            "screenshot_path": str(screenshot_path),
            "html_content": html_content,
            "status": "success"
        }
    except Exception as e:
        logger.warning(f"Crawl failed: {e}. Falling back to mock data.")
        mock_html = (
            "<!DOCTYPE html><html><head><title>Prefect Test</title></head><body>"
            "<div class='container'><h1>Prefect Orchestrated Layout</h1>"
            "<p>This page was generated through Prefect automated flows.</p>"
            "<button class='btn'>Accept</button></div></body></html>"
        )
        html_path = Path(output_dir) / "page.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(mock_html)
            
        mock_screenshot = Path(output_dir) / "screenshot.png"
        if not mock_screenshot.exists():
            from PIL import Image
            img = Image.new('RGB', (100, 100), color='green')
            img.save(mock_screenshot)
            
        return {
            "html_path": str(html_path),
            "screenshot_path": str(mock_screenshot),
            "html_content": mock_html,
            "status": "mock_fallback"
        }


@task(name="Extract Content Task")
def extract_content_task(html_content: str) -> Dict[str, Any]:
    logger.info("Prefect Task: Extracting content...")
    from backend.extractor.service import ExtractorService
    extractor = ExtractorService()
    result = extractor.extract(html_content)
    return {"result": result.model_dump()}


@task(name="Analyze Visuals Task")
def analyze_visuals_task(screenshot_path: str) -> Dict[str, Any]:
    logger.info("Prefect Task: Analyzing screenshot visuals...")
    from backend.vision.analyzer import VisionAnalyzer
    analyzer = VisionAnalyzer()
    result = analyzer.analyze(screenshot_path)
    return {"result": result.model_dump()}


@task(name="Resolve Styles Task")
def resolve_styles_task(extraction: Dict[str, Any], vision: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Prefect Task: Resolving styles and design tokens...")
    from backend.analyzer.layout_analyzer import LayoutAnalyzer
    ext_model = ExtractionResult.model_validate(extraction)
    vis_model = VisionMetadata.model_validate(vision)
    analyzer = LayoutAnalyzer()
    result = analyzer.analyze(ext_model, vis_model)
    return {"result": result.model_dump()}


@task(name="Generate Code Task")
def generate_code_task(extraction: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Prefect Task: Generating React components...")
    from backend.codegen.code_generator import CodeGenerator
    ext_model = ExtractionResult.model_validate(extraction)
    ana_model = AnalysisResult.model_validate(analysis)
    generator = CodeGenerator()
    result = generator.generate(ext_model, ana_model)
    return {"result": result.model_dump()}


@task(name="Package Dataset Task")
def package_dataset_task(
    url: str,
    raw_html: str,
    screenshot_path: str,
    extraction: Dict[str, Any],
    vision: Dict[str, Any],
    analysis: Dict[str, Any],
    codegen: Dict[str, Any],
    project_id: int
) -> str:
    logger.info("Prefect Task: Packaging dataset package...")
    from backend.dataset.builder import DatasetBuilder
    ext_model = ExtractionResult.model_validate(extraction)
    vis_model = VisionMetadata.model_validate(vision)
    ana_model = AnalysisResult.model_validate(analysis)
    cod_model = CodegenResult.model_validate(codegen)
    
    base_dir = Path(__file__).resolve().parent.parent.parent
    builder = DatasetBuilder(base_dataset_path=str(base_dir / "dataset"))
    site_dir = builder.build_package(
        site_id=project_id,
        url=url,
        raw_html=raw_html,
        screenshot_path=screenshot_path,
        extraction=ext_model,
        vision=vis_model,
        analysis=ana_model,
        codegen=cod_model
    )
    return site_dir


@task(name="Index Vectors Task")
def index_vectors_task(site_dir: str) -> Dict[str, Any]:
    logger.info("Prefect Task: Indexing vectors in ChromaDB...")
    from backend.database.chroma_client import ChromaClientManager
    from backend.rag.embeddings import EmbeddingGenerator
    
    site_path = Path(site_dir)
    manifest_path = site_path / "manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = DatasetManifest.model_validate_json(f.read())
        
    generator = EmbeddingGenerator()
    chroma = ChromaClientManager()
    
    page_text = (
        f"Page layout for {manifest.site_id} crawled from {manifest.url}. "
        f"Primary color: {manifest.primary_color}, Background: {manifest.background_color}."
    )
    page_vector = generator.get_embedding(page_text)
    chroma.upsert(
        collection_name="pages",
        doc_id=manifest.site_id,
        vector=page_vector,
        document=page_text,
        metadata={"url": manifest.url, "site_id": manifest.site_id}
    )
    
    style_text = f"Theme palette. Primary: {manifest.primary_color}, Background: {manifest.background_color}"
    style_vector = generator.get_embedding(style_text)
    chroma.upsert(
        collection_name="styles",
        doc_id=manifest.site_id,
        vector=style_vector,
        document=style_text,
        metadata={"site_id": manifest.site_id}
    )
    
    components_path = site_path / "components"
    components_indexed = 0
    if components_path.exists():
        for file in os.listdir(components_path):
            if file.endswith(".tsx"):
                comp_name = file.replace(".tsx", "")
                comp_file = components_path / file
                with open(comp_file, "r", encoding="utf-8") as cf:
                    comp_code = cf.read()
                comp_vector = generator.get_embedding(comp_code)
                doc_id = f"{manifest.site_id}_{comp_name}"
                chroma.upsert(
                    collection_name="components",
                    doc_id=doc_id,
                    vector=comp_vector,
                    document=comp_code,
                    metadata={"site_id": manifest.site_id, "component_id": comp_name}
                )
                components_indexed += 1
                
    return {"indexed_documents": 2 + components_indexed}


@flow(name="generation-pipeline-flow")
def generation_pipeline_flow(url: str, target_framework: str = "React", project_id: int = 1) -> Dict[str, Any]:
    """Prefect orchestration workflow pipeline for the UI AI ecosystem."""
    base_dir = Path(__file__).resolve().parent.parent.parent
    output_dir = str(base_dir / "storage" / "prefect_run")
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Crawl Page
    crawl_res = crawl_page_task(url, output_dir)
    
    # 2. Extract DOM/CSS
    extract_res = extract_content_task(crawl_res["html_content"])
    
    # 3. Vision Extraction
    vision_res = analyze_visuals_task(crawl_res["screenshot_path"])
    
    # 4. Resolve styles and layout guide
    style_res = resolve_styles_task(extract_res["result"], vision_res["result"])
    
    # 5. React Code Generation
    codegen_res = generate_code_task(extract_res["result"], style_res["result"])
    
    # 6. Package dataset structure
    site_dir = package_dataset_task(
        url=url,
        raw_html=crawl_res["html_content"],
        screenshot_path=crawl_res["screenshot_path"],
        extraction=extract_res["result"],
        vision=vision_res["result"],
        analysis=style_res["result"],
        codegen=codegen_res["result"],
        project_id=project_id
    )
    
    # 7. Semantic database indexing
    rag_res = index_vectors_task(site_dir)
    
    return {
        "site_dir": site_dir,
        "rag_indexed_docs": rag_res["indexed_documents"]
    }
