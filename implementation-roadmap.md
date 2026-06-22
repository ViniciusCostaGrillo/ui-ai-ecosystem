FASE 1 — Inicialização

Criar:

ui-ai/
backend/
frontend/
dataset/
docker/
logs/
storage/
configs/

Inicializar Git.

Criar:

.gitignore
README.md
docker-compose.yml
.env.example
FASE 2 — Ambiente Python

Criar venv.

Instalar:

FastAPI
SQLAlchemy
Redis
Playwright
Crawl4AI
Firecrawl
BeautifulSoup
lxml
Trafilatura
ChromaDB
sentence-transformers
LangGraph
PydanticAI
Agno
Prefect
Airflow
Unsloth
Llama Factory

Gerar requirements.txt.

FASE 3 — Frontend

Criar projeto Next.js.

Instalar:

Tailwind
Shadcn
TypeScript
Monaco Editor
TanStack Query
Zustand
FASE 4 — Docker

Criar containers:

api
postgres
redis
chromadb
frontend
workers
prefect
FASE 5 — PostgreSQL

Criar tabelas:

Users

Projects

Executions

Jobs

Logs

Datasets

CrawlerHistory

TrainingHistory

FASE 6 — API

Criar endpoints:

POST /generate

POST /crawl

POST /analyze

POST /codegen

POST /dataset

GET /projects

GET /components

GET /styles

FASE 7 — Crawlers

Implementar:

PlaywrightEngine

Crawl4AIEngine

FirecrawlEngine

FASE 8 — Extractor

Implementar:

HTML Parser

CSS Parser

Text Parser

Metadata Parser

FASE 9 — Vision

Extrair:

cores
grids
espaçamento
densidade visual

Produzir:

vision_metadata.json

FASE 10 — Analyzer

Utilizar:

Gemini

GPT

Claude

Produzir:

metadata.json

FASE 11 — Codegen

Converter:

HTML

↓

React + Tailwind

Produzir componentes.

FASE 12 — Dataset Builder

Criar:

site_000001/

site_000002/

...

FASE 13 — Embeddings

Gerar embeddings para:

páginas
componentes
estilos
FASE 14 — ChromaDB

Criar coleções.

Implementar busca semântica.

FASE 15 — Multiagentes

Implementar:

LangGraph

PydanticAI

Agno

FASE 16 — Pipeline LangGraph

CrawlerAgent

↓

ExtractorAgent

↓

VisionAgent

↓

StyleAgent

↓

CodeAgent

↓

DatasetAgent

↓

RagAgent

FASE 17 — Workers

Redis Queue

Processamento paralelo.

FASE 18 — Prefect

Criar flows automáticos.

FASE 19 — Airflow

Criar DAGs.

Executar processamento diário.

FASE 20 — RAG

Prompt

↓

Embeddings

↓

ChromaDB

↓

Top-K

↓

LLM

↓

Resposta

FASE 21 — Frontend

Criar:

Editor

Preview

Projects

History

Logs

Settings

FASE 22 — Training

Implementar:

Unsloth

Llama Factory

LoRA

Versionamento

Experimentos

FASE 23 — Observabilidade

Logs

Tracing

Retries

Health Checks

FASE 24 — Escalabilidade

Workers

Redis

Sharding

Cache

Background Tasks

FASE 25 — Sistema Completo

Prompt

↓

RAG

↓

LLM

↓

React + Tailwind

↓

Preview

↓

Projeto salvo

↓

Dataset cresce continuamente

Regras para o agente
Nunca pular fases.
Aplicar SOLID.
Utilizar Clean Architecture.
Criar testes unitários.
Utilizar Pydantic em todos os schemas.
Criar logs em todos os serviços.
Criar tratamento de exceções.
Utilizar Docker em todos os módulos.
Priorizar escalabilidade horizontal.
Construir um sistema semelhante ao Lovable, Bolt e v0.
