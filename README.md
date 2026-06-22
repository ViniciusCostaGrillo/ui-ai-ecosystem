# UI AI Ecosystem 🚀

An AI-driven design system learning and website code generator similar to **Lovable, Bolt, and v0**, engineered to extract visual patterns from existing websites and utilize RAG (Retrieval-Augmented Generation) to build modern React + Tailwind components.

---

## 🏗️ Project Architecture

```
ui-ai-builder/
├── backend/                  # Python FastAPI Backend
│   ├── api/                  # Endpoints (generate, crawl, codegen, etc.)
│   ├── agents/               # Multi-agent architecture (LangGraph, PydanticAI)
│   ├── crawler/              # Web scraping engines (Playwright, Crawl4AI, Firecrawl)
│   ├── extractor/            # Clean text/HTML/CSS parsing
│   ├── vision/               # Computer vision heuristics (grid, colors, spacing)
│   ├── analyzer/             # LLM orchestration (Gemini, GPT, Claude)
│   ├── codegen/              # Output React + Tailwind component generation
│   ├── rag/                  # Semantic search search and indexing
│   ├── training/             # Fine-tuning engines (Unsloth, Llama Factory)
│   ├── workers/              # Redis tasks queue workers
│   ├── database/             # PostgreSQL schemas & SQLAlchemy models
│   ├── services/             # Core utility services
│   ├── schemas/              # Pydantic schema validation
│   └── utils/                # Logging, exception handling, and helpers
├── frontend/                 # Next.js TypeScript Frontend application
├── dataset/                  # Extracted website pages assets
├── docker/                   # Dockerfiles configuration files
├── storage/                  # Generated assets and model files
├── logs/                     # System logs outputs
├── configs/                  # General deployment configs
├── scripts/                  # Management scripts
├── docs/                     # Specifications and references
└── models/                   # Local models cache (sentence-transformers)
```

---

## 🛠️ Technology Stack

### Backend
* **Language:** Python 3.12+
* **Framework:** FastAPI
* **Database:** PostgreSQL (with SQLAlchemy ORM)
* **Caching & Queue:** Redis
* **Vector Store:** ChromaDB (with sentence-transformers)

### Agents & Parsing
* **Multi-agent Orchestration:** LangGraph, PydanticAI, Agno
* **Crawlers:** Playwright, Crawl4AI, Firecrawl
* **HTML/CSS Extraction:** BeautifulSoup4, lxml, Trafilatura

### Fine-Tuning
* **Frameworks:** Unsloth, Llama Factory (LoRA adapters)

### Frontend
* **Framework:** Next.js (TypeScript)
* **Styling:** TailwindCSS & shadcn/ui
* **State Management:** Zustand & TanStack Query
* **Editor:** Monaco Editor

---

## ⚙️ Quick Start

### 1. Requirements
Ensure you have the following installed:
* [Docker & Docker Compose](https://www.docker.com/)
* [Python 3.12+](https://www.python.org/)
* [Node.js v20+](https://nodejs.org/)

### 2. Environment Setup
Clone the repository and copy the environment example template:
```bash
cp .env.example .env
```
Fill in the necessary API keys (`GEMINI_API_KEY`, `OPENAI_API_KEY`, etc.) inside the newly created `.env` file.

### 3. Spin up Infrastructure
Run the containerized services using Docker Compose:
```bash
docker compose up --build -d
```
This starts:
* **PostgreSQL** on port `5432`
* **Redis** on port `6379`
* **ChromaDB** on port `8000` (Vector search API)
* **API Backend** on port `8000`
* **Frontend** on port `3000`
* **Queue Workers** for background scraping and extraction processing.

---

## 📄 Development Guidelines
* **Architecture:** Adhere strictly to **Clean Architecture** and **SOLID** principles.
* **Validation:** Every input/output schema must be strictly typed using **Pydantic**.
* **Quality Assurance:** Run local linting and type checks (`npm run lint` and `ruff check .`) before pushing code.
* **Testing:** Write comprehensive unit and integration tests under `tests/` directories.
