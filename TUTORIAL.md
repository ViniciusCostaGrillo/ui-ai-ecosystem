# Helix UI AI Builder: System & Usage Tutorial

Welcome to the **Helix UI AI Builder**! This tutorial provides a comprehensive guide on how to configure, run, test, and use the ecosystem's features—spanning the AI Designer Engine, the Knowledge Hub crawler, the FastAPI backend services, and the Next.js frontend dashboard.

---

## 1. System Ecosystem Overview

The Helix UI AI Builder is structured into four main layers:

```
┌────────────────────────────────────────────────────────┐
│               Next.js UI Frontend Dashboard            │
└───────────┬────────────────────────────────┬───────────┘
            │                                │
            ▼ (REST APIs)                    ▼ (REST APIs)
┌──────────────────────┐          ┌──────────────────────┐
│  Designer Engine API │          │  Website Importer API│
└───────────┬──────────┘          └───────────┬──────────┘
            │                                │
            ▼ (Vector RAG Search)            ▼ (Ingestion Pipelines)
┌────────────────────────────────────────────────────────┐
│  ChromaDB + SentenceTransformers (all-MiniLM-L6-v2)    │
└────────────────────────────────────────────────────────┘
```

1.  **Designer Intelligence Engine**: Compiles design plans (block structures, typography, spacing profiles, animations presets) before code generation based on semantic prompts.
2.  **Website Ingestion (Knowledge Hub)**: Leverages headless Playwright crawlers to extract CSS design systems, typography configurations, grids, animations, and assets from reference URLs.
3.  **Masterpiece Registry**: Promotes high-quality references (Awwwards-level designs like Stripe, Linear, Elara) to prioritize their layout components during retrieval-augmented code generation (RAG).
4.  **ChromaDB Vector Store**: Semantic database storing embeddings of layouts, components, design rules, and prompt configurations.

---

## 2. Setup & Installation

Follow these steps to run the backend and frontend locally:

### Python Backend Setup
1.  **Create and Activate Virtual Environment**:
    ```bash
    python -m venv .venv
    # Windows PowerShell:
    .venv\Scripts\Activate.ps1
    # Linux/macOS:
    source .venv/bin/activate
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    ```
3.  **Database Migration & Seeding**:
    Initialize tables in the SQLite database and seed default masterpiece templates:
    ```bash
    $env:DATABASE_URL="sqlite:///./test.db"
    $env:ANALYTICS_DATABASE_URL="sqlite:///./test_analytics.db"
    python -m backend.utils.init_db
    ```

### Next.js Frontend Setup
1.  **Install Packages**:
    Navigate to the frontend folder and install npm packages:
    ```bash
    cd frontend
    npm install --legacy-peer-deps
    ```
2.  **Run Development Server**:
    ```bash
    npm run dev
    ```

---

## 3. Using the Frontend Knowledge Hub Dashboard

When you navigate to the **Knowledge Hub** module in the Next.js workspace, you are presented with a modern dark-mode control center:

### A. Left Sidebar Navigation
*   **Import Center**: Your starting point for url imports and file batch uploads.
*   **Masterpieces (GSAP/3D)**: Displays outstanding reference sites. Allows manual additions, promotions, and demotions.
*   **Library Explorer**: An interactive tree browser displaying components, design systems, assets, and skills currently indexed.
*   **Growth Analytics**: Displays area charts of crawled references/components over time and pie charts of categorical distributions.
*   **Crawler Settings**: Configuration form to edit watchdog schedules, whitelist domains, AI models, and RAG weights.

### B. Uploading Batch References
To upload multiple reference URLs at once:
1.  Create a `.txt` file containing one URL per line, or a `.csv` file with column headers `Name,URL,Category,Priority`.
2.  Drag and drop the file into the **Batch File Reference Import** dashboard box.
3.  The system parses the URLs, filters duplicates, and automatically enqueues Playwright scraper jobs.

### C. Live Ingestion Queue & Logs
*   **Queue Tracker**: Watch active crawling jobs in real-time. The stage indicator updates dynamically: `Crawl ➔ HTML ➔ Assets ➔ Motion ➔ Knowledge ➔ Embeddings ➔ Ready`.
*   **Console Logs**: View crawler worker output in real-time. Use the search bar and status drop-down (Info, Warning, Success) to filter logs.

---

## 4. Backend REST API Reference

The FastAPI backend exposes several key HTTP endpoints:

### Designer Engine (`/designer`)
*   `POST /designer/plan`
    *   **Description**: Compiles prompt requests into semantic layout blocks, style tags, and motion guidelines.
    *   **Payload**: `{ "prompt": "Create a luxury footwear ecommerce website" }`

### Website Ingestion (`/importer`)
*   `POST /importer/url`
    *   **Description**: Queues a single target URL for playwrighter crawling and design indexing.
    *   **Payload**: `{ "url": "https://stripe.com", "promote_to_masterpiece": true, "category": "fintech" }`
*   `POST /importer/upload`
    *   **Description**: Accepts a CSV, TXT, or JSON file upload containing batch URLs.
*   `GET /importer/queue`
    *   **Description**: Returns active and completed crawl job progress reports.
*   `GET /importer/stats`
    *   **Description**: Aggregates database totals for crawled sites, assets, design systems, and vector embeddings.
*   `POST /importer/promote`
    *   **Description**: Manually promotes an ingested URL to masterpiece reference status.
*   `POST /importer/demote`
    *   **Description**: Removes masterpiece status from a reference URL.

---

## 5. Running CLI Verification Tests

You can verify the system's functions by running the Python test scripts:

### Run Designer Engine Tests
```bash
$env:DATABASE_URL="sqlite:///./test.db"
$env:ANALYTICS_DATABASE_URL="sqlite:///./test_analytics.db"
python -m backend.utils.test_designer_engine
```

### Run Masterpiece Engine Tests
```bash
$env:DATABASE_URL="sqlite:///./test.db"
$env:ANALYTICS_DATABASE_URL="sqlite:///./test_analytics.db"
python -m backend.utils.test_masterpiece_engine
```

### Run Website Importer Tests
```bash
$env:DATABASE_URL="sqlite:///./test.db"
$env:ANALYTICS_DATABASE_URL="sqlite:///./test_analytics.db"
python -m backend.utils.test_importer_engine
```

---

## 6. System Diagnostics & Performance Tuning

### ChromaDB and Redis Singletons
To prevent connection overhead, the backend contains connection caching classes.
*   **ChromaDB Caching**: `ChromaClientManager` caches local PersistentClient connections, eliminating repeated initialization delays.
*   **Neural Network Caching**: `EmbeddingGenerator` caches `SentenceTransformer` models, so the weights are loaded only once in memory.
*   **Locking safety**: `QueueManager` uses `threading.RLock()` (Re-entrant Lock), preventing thread deadlocks during recursive requests.
