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


# UPDATE — PHASE 26 & PHASE 27

---

# PHASE 26 — ADVANCED MOTION ENGINE

## Objetivo

Permitir que o sistema produza experiências visuais comparáveis aos melhores sites do:

* Awwwards
* FWA
* Refokus
* Active Theory
* Obys
* Locomotive
* Holographik

---

# Motion Engine

Criar:

```txt
backend/motion/

motion_agent/
gsap_agent/
lenis_agent/
lottie_agent/
parallax_agent/
transition_agent/
microinteraction_agent/
```

---

# ThreeJS Engine

Criar:

```txt
backend/threejs/

threejs_agent/
r3f_agent/
shader_agent/
particles_agent/
```

---

# Dependency Manager

Criar:

```txt
backend/dependencies/

dependency_agent/
package_registry/
package_validator/
```

Instalação automática de:

* motion
* gsap
* lenis
* three
* @react-three/fiber
* @react-three/drei
* lottie-react

---

# Animation Dataset

Gerar:

```txt
animations.json

dependencies.json

motion_metadata.json
```

---

# Animation Collections

Adicionar ao ChromaDB:

* AnimationPatterns
* MotionComponents
* GSAPTimelines
* ThreeJSScenes
* Dependencies

---

# PHASE 27 — KNOWLEDGE & DESIGN SYSTEMS ENGINE

## Objetivo

Construir uma base de conhecimento viva inspirada em:

* Aura Assets
* Aura Skills
* Aura Design Systems

---

# Asset Engine

Criar:

```txt
backend/assets/

asset_agent/
asset_library/
backgrounds/
gradients/
textures/
3d_assets/
icons/
videos/
```

---

# Skill Engine

Criar:

```txt
backend/skills/

skill_engine/

luxury_skill/
saas_skill/
ai_skill/
dashboard_skill/
agency_skill/
portfolio_skill/
threejs_skill/
motion_skill/
```

---

# Design Systems Engine

Criar:

```txt
design_systems/

luxury/
saas/
portfolio/
dashboard/
startup/
agency/
minimal/
glassmorphism/
```

---

# Component Library

Criar:

```txt
component_library/

hero/
navbar/
cards/
pricing/
footer/
gallery/
dashboard/
faq/
```

---

# Theme Engine

Criar:

```txt
backend/themes/

theme_agent/

dark_theme/
light_theme/
luxury_theme/
glass_theme/
minimal_theme/
```

---

# Knowledge Ingestion Engine

## Objetivo

Detectar automaticamente novos materiais adicionados pelo usuário.

Criar:

```txt
backend/knowledge/

knowledge_ingestion/

knowledge_builder/

knowledge_scheduler/

knowledge_registry/

knowledge_watchdog/
```

---

# Pasta monitorada

```txt
knowledge_input/

assets/

components/

design_systems/

skills/

prompt_templates/

images/

videos/

3d/

references/
```

---

# Funcionamento

Todos os dias:

09:00

↓

Knowledge Scheduler

↓

Verifica se houve novos arquivos

↓

Se houver

↓

Envia para Knowledge Builder Agent

↓

Extrai conhecimento

↓

Atualiza ChromaDB

↓

Atualiza dataset

↓

Expande biblioteca

---

# Knowledge Builder Agent

Responsabilidades:

* analisar arquivos novos
* identificar tipo do material
* gerar metadata
* gerar embeddings
* gerar DESIGN.md
* gerar skill.yaml
* atualizar component library
* atualizar assets
* atualizar themes

---

# Tipos suportados

Imagens

```txt
png
jpg
jpeg
svg
webp
```

Vídeos

```txt
mp4
mov
webm
```

3D

```txt
glb
gltf
obj
```

Código

```txt
tsx
jsx
html
css
scss
```

Configurações

```txt
json
yaml
yml
md
```

---

# Auto Knowledge Generation

Exemplo:

Usuário adiciona:

```txt
knowledge_input/

references/

premium_hero.png
```

↓

Knowledge Builder Agent

↓

Vision Agent

↓

Extrai:

* paleta
* tipografia
* layout
* animações

↓

Gera:

```txt
design_systems/

luxury/

colors.json

typography.json

spacing.json

motion.json

DESIGN.md
```

---

# Auto Skill Generation

Se identificar um padrão recorrente:

Gerar:

```txt
skills/

luxury_skill/

skill.yaml
```

---

# Auto Component Generation

Se encontrar:

* Hero
* Footer
* Cards
* Pricing

Gerar:

```txt
component_library/

hero/

hero_0124.tsx

hero_0124_metadata.json
```

---

# Knowledge Collections

Adicionar ao ChromaDB:

* Assets
* Skills
* Themes
* DesignSystems
* Components
* MotionPresets
* PromptTemplates

---

# Knowledge Watchdog

Criar serviço permanente:

```txt
backend/knowledge/watchdog/
```

Responsabilidade:

Monitorar continuamente:

```txt
knowledge_input/
```

Quando detectar novos arquivos:

↓

Criar Job Redis

↓

Executar Knowledge Builder Agent

↓

Atualizar ChromaDB

↓

Atualizar Dataset

↓

Atualizar Bibliotecas

---

# Daily Knowledge Scan

Criar Flow no Prefect:

DailyKnowledgeFlow

Executar:

Todo dia às 09:00

Todo dia às 18:00

---

# Pipeline

Knowledge Input

↓

Knowledge Watchdog

↓

Knowledge Builder Agent

↓

Vision Agent

↓

Style Agent

↓

Embedding Agent

↓

ChromaDB

↓

Design System Engine

↓

Skill Engine

↓

Asset Engine

↓

Component Library

↓

Dataset cresce continuamente

---

# Objetivo Final

O usuário poderá simplesmente copiar arquivos para:

```txt
knowledge_input/
```

e o sistema estudará automaticamente tudo o que foi adicionado, transformando os materiais em conhecimento reutilizável, expandindo continuamente a inteligência da plataforma sem necessidade de intervenção manual.


# Masterpiece Engine ⭐

## Objetivo

Permitir que determinados sites, templates e designs sejam promovidos para a categoria especial de **MASTERPIECE** ou **GOLDEN_REFERENCE**, recebendo um nível de análise muito mais profundo do que os sites normais do dataset.

Esses designs passam a ser considerados referências de altíssimo valor e terão maior influência nas buscas RAG e na geração de novos projetos.

---

# Estrutura

Criar:

```txt
backend/masterpieces/

masterpiece_agent/
masterpiece_registry/
masterpiece_builder/
masterpiece_embeddings/
masterpiece_validator/
masterpiece_library/
```

---

# Registro de Masterpieces

Criar:

```txt
masterpieces/

elara/
noirframe/
linear/
stripe/
vercel/
refokus/
obys/
active_theory/
```

---

# masterpiece.yaml

Exemplo:

```yaml
name: Elara Footwear

priority: masterpiece

category:
  - fashion
  - luxury
  - ecommerce

analyze_depth: maximum

generate:

  - design_system
  - skills
  - assets
  - components
  - animations
  - dependencies
  - prompt_templates
  - themes
  - typography
  - color_palettes

weight: 10
```

---

# Masterpiece Collections

Adicionar ao ChromaDB:

```txt
Masterpieces

MasterpieceComponents

MasterpieceAnimations

MasterpieceAssets

MasterpieceDesignSystems

GoldenReferences
```

---

# Weight System

Componentes normais:

```txt
weight = 1
```

Componentes provenientes de Masterpieces:

```txt
weight = 10
```

A busca semântica deverá priorizar referências oriundas dos Masterpieces.

---

# Masterpiece Builder Agent

Quando um site for promovido para MASTERPIECE, executar:

```txt
URL

↓

Playwright

↓

Screenshots

↓

HTML

↓

Vision Agent

↓

Style Agent

↓

Animation Agent

↓

Typography Agent

↓

Color Agent

↓

Asset Agent

↓

Theme Agent

↓

Knowledge Builder Agent

↓

Masterpiece Builder Agent

↓

ChromaDB
```

---

# Estrutura Gerada

Cada Masterpiece deverá produzir:

```txt
masterpieces/

elara/

DESIGN.md

skill.yaml

colors.json

typography.json

motion.json

theme.json

assets/

components/

animations/

prompts/

embeddings/
```

---

# Masterpiece Tags

Exemplo:

```json
{
  "masterpiece": true,
  "priority": 10,
  "style": [
    "luxury",
    "editorial",
    "fashion"
  ]
}
```

---

# Prompt Templates

Gerar:

```txt
prompt_templates/

elara.md

noirframe.md

linear.md

stripe.md

refokus.md
```

---

# Super Skills

Gerar automaticamente:

```txt
skills/

elara_skill/

noirframe_skill/

linear_skill/

stripe_skill/

refokus_skill/
```

---

# Masterpiece Dashboard

Adicionar ao frontend:

```txt
Masterpieces

⭐ Elara Footwear

⭐ NoirFrame Fashion

⭐ Linear

⭐ Stripe

⭐ Vercel

⭐ Refokus
```

Permitir:

```txt
Promote to Masterpiece

Demote from Masterpiece
```

---

# Masterpiece Score

Cada referência deverá receber uma pontuação baseada em:

* Visual Quality
* Typography
* Spacing
* Motion
* Components
* Color Harmony
* Accessibility
* Performance
* Responsiveness

Exemplo:

```txt
Overall Score: 98.4
```

---

# Manual Promotion

O usuário poderá executar:

```txt
Analyze as MASTERPIECE:

https://www.aura.build/templates/elara-footwear
```

ou

```txt
Promote to MASTERPIECE:

https://noirframefashion.aura.build/
```

---

# Objetivo Final

Construir uma coleção de referências premium capazes de servir como os principais "professores" do sistema.

Os Masterpieces terão prioridade sobre o restante do dataset e serão responsáveis por fornecer:

* Design Systems de alta qualidade;
* Skills avançadas;
* Motion Patterns;
* Assets premium;
* Componentes reutilizáveis;
* Prompt Templates especializados;
* Conhecimento de nível Awwwards.

Com o passar do tempo, os Masterpieces se tornarão o núcleo de conhecimento mais valioso de toda a plataforma.


# PHASE 28 — DESIGNER INTELLIGENCE ENGINE

## Objetivo

Transformar a plataforma de um simples gerador de interfaces em um verdadeiro sistema de direção criativa assistida por IA.

A Fase 28 introduz uma camada de inteligência responsável por interpretar intenções visuais, selecionar referências, construir estratégias de design e planejar a experiência antes da geração de código.

O foco desta fase não é gerar código diretamente, mas sim tomar decisões de design de alto nível da mesma forma que um Diretor de Arte, Product Designer ou Creative Director faria.

---

# Objetivos Principais

* Entender objetivos de negócio.
* Entender o público-alvo.
* Entender o contexto do projeto.
* Construir estratégias visuais.
* Selecionar referências automaticamente.
* Montar moodboards.
* Definir Design Systems.
* Planejar layouts.
* Planejar animações.
* Planejar experiência do usuário.
* Guiar os agentes de geração.

---

# Estrutura

Criar:

```txt
backend/designer/

designer_agent/

creative_director_agent/

moodboard_engine/

visual_planning_engine/

style_composer/

reference_composer/
```

---

# Designer Agent

## Objetivo

Interpretar o prompt do usuário e transformá-lo em uma intenção visual estruturada.

Exemplo:

Prompt:

```text
Create a luxury footwear ecommerce website.
```

Resultado:

```yaml
industry: fashion

category: ecommerce

style:
  - luxury
  - editorial
  - premium

theme:
  - light

animations:
  - subtle

priority:
  - typography
  - product showcase
```

---

# Creative Director Agent

## Objetivo

Atuar como um Diretor de Arte virtual.

Responsabilidades:

* Definir direção criativa.
* Escolher referências.
* Definir identidade visual.
* Escolher estilos.
* Escolher tipografias.
* Escolher paletas.
* Escolher animações.
* Escolher assets.
* Definir hierarquia visual.

---

# Moodboard Engine

## Objetivo

Montar moodboards automáticos com base no projeto solicitado.

Criar:

```txt
knowledge/

moodboards/

luxury/
fashion/
editorial/
saas/
startup/
agency/
ai/
dashboard/
minimal/
glassmorphism/
```

---

# Estrutura do Moodboard

```json
{
  "style": "luxury",

  "colors": [
    "#0F0F0F",
    "#D4AF37"
  ],

  "typography": [
    "Playfair Display",
    "Inter"
  ],

  "references": [
    "elara",
    "noirframe"
  ]
}
```

---

# Visual Planning Engine

## Objetivo

Criar um plano visual completo antes da geração de código.

Pipeline:

```text
Prompt

↓

Designer Agent

↓

Creative Director Agent

↓

Visual Planning Engine

↓

Code Agent
```

---

# Exemplo de Plano Visual

```yaml
layout:
  hero
  gallery
  products
  testimonials
  footer

theme:
  luxury

spacing:
  large

animations:
  gsap

scroll:
  lenis

background:
  premium_gradient

references:
  elara
  noirframe
```

---

# Style Composer

## Objetivo

Combinar diferentes estilos para criar novas identidades visuais.

Exemplo:

```text
Luxury

+

Glassmorphism

+

Editorial

+

Minimalism
```

↓

Resultado:

```yaml
style:
  luxury-editorial-glass
```

---

# Reference Composer

## Objetivo

Combinar referências armazenadas no sistema.

Fontes possíveis:

* Masterpieces
* Design Systems
* Skills
* Assets
* Component Library
* Motion Library

---

# Exemplo

Entrada:

```text
Elara Footwear

+

NoirFrame Fashion

+

Refokus
```

Saída:

```yaml
references:
  - elara
  - noirframe
  - refokus

merged_style:
  luxury-editorial-modern
```

---

# Integração com Masterpieces

O Designer Intelligence Engine deverá priorizar referências provenientes dos Masterpieces.

Coleções prioritárias:

* Masterpieces
* MasterpieceComponents
* MasterpieceAssets
* MasterpieceAnimations
* MasterpieceDesignSystems

---

# Integração com Knowledge Engine

Consultar:

* Assets
* Skills
* Design Systems
* Themes
* Components
* Animations
* Prompt Templates

Antes de iniciar qualquer geração.

---

# Designer Workflow

```text
Prompt

↓

Designer Agent

↓

Creative Director Agent

↓

Moodboard Engine

↓

Style Composer

↓

Reference Composer

↓

Visual Planning Engine

↓

Code Agent

↓

Preview
```

---

# Objetivo Final

Permitir que a plataforma pense como um designer antes de agir como um desenvolvedor.

Ao invés de simplesmente gerar componentes, o sistema será capaz de:

* Planejar experiências.
* Construir identidades visuais.
* Selecionar referências.
* Criar estratégias de design.
* Produzir interfaces mais coerentes.
* Produzir interfaces mais criativas.
* Produzir interfaces dignas de premiações.

A Fase 28 representa a transição da plataforma de um gerador de interfaces para um verdadeiro Diretor de Arte alimentado por Inteligência Artificial.

# PHASE 29 — WEBSITE IMPORT CENTER

# Objetivo

Criar um módulo completo para importação, gerenciamento e análise em massa de websites.

O Website Import Center será a principal porta de entrada de conhecimento da plataforma.

Seu objetivo é permitir que o usuário importe centenas ou milhares de URLs utilizando arquivos TXT, CSV ou JSON, iniciando automaticamente todo o pipeline de análise, enriquecimento de conhecimento e armazenamento.

---

# Estrutura

Criar:

backend/importer/

website_importer/
url_parser/
batch_processor/
import_scheduler/
import_validator/
queue_manager/

frontend/

app/import/

components/

ImportCard.tsx
ImportHistory.tsx
ImportQueue.tsx
ImportProgress.tsx
ImportSettings.tsx

---

# Interface

Adicionar uma nova página:

Knowledge

↓

Website Import Center

A interface deverá possuir:

──────────────────────────────────────

Website Import Center

[ Upload TXT ]

[ Upload CSV ]

[ Upload JSON ]

ou

Cole uma URL:

_________________________________

[ Analyze ]

──────────────────────────────────────

Batch Options

☑ Generate Design Systems

☑ Generate Skills

☑ Extract Components

☑ Extract Assets

☑ Analyze Animations

☑ Generate Prompt Templates

☑ Generate Embeddings

☑ Save to ChromaDB

☑ Promote imported websites to Masterpiece

──────────────────────────────────────

Import Queue

Waiting

Running

Completed

Failed

──────────────────────────────────────

Progress

██████████░░░░░░░░ 52%

Site 53 of 100

──────────────────────────────────────

---

# Upload TXT

O sistema deverá aceitar arquivos:

.txt

Formato:

https://linear.app

https://stripe.com

https://vercel.com

https://www.aura.build/templates/elara-footwear

https://noirframefashion.aura.build

Uma URL por linha.

Linhas vazias devem ser ignoradas.

Linhas duplicadas devem ser removidas automaticamente.

---

# Upload CSV

Formato:

Name,URL,Category,Priority

Linear,https://linear.app,saas,masterpiece

Stripe,https://stripe.com,fintech,normal

Elara,https://www.aura.build/templates/elara-footwear,fashion,masterpiece

---

# Upload JSON

Formato:

[
    {
        "url":"https://linear.app",
        "category":"saas",
        "priority":"masterpiece"
    },
    {
        "url":"https://stripe.com"
    }
]

---

# Pipeline

Upload

↓

Validation

↓

URL Parser

↓

Deduplication

↓

Redis Queue

↓

Playwright

↓

HTML Extractor

↓

Asset Extractor

↓

Component Analyzer

↓

Motion Analyzer

↓

Knowledge Builder

↓

Embedding Generator

↓

ChromaDB

↓

Finished

---

# URL Validation

Antes de iniciar a análise:

✓ URL válida

✓ HTTPS

✓ Não duplicada

✓ Não analisada recentemente

✓ Domínio permitido

---

# Deduplication

Evitar:

URL duplicada

Domínio duplicado

Redirecionamentos repetidos

Mesmo site em múltiplos arquivos

---

# Queue System

Cada URL deverá gerar um Job.

Exemplo:

Job #123

Status: Waiting

↓

Running

↓

Completed

↓

Stored

---

# Progress Dashboard

Mostrar:

Sites totais

Sites analisados

Sites restantes

Tempo estimado

Velocidade

Falhas

Assets extraídos

Componentes encontrados

Design Systems gerados

Skills geradas

Embeddings criados

---

# Histórico

Criar:

Knowledge

↓

Import History

Mostrar:

Data

Arquivo importado

Quantidade de URLs

Tempo

Status

Botão:

Analyze Again

---

# Masterpiece Detection

Durante a importação:

Caso o arquivo indique:

priority = masterpiece

ou

category = masterpiece

O sistema deverá enviar automaticamente o site para o Masterpiece Engine.

---

# Regras

Nunca analisar o mesmo site duas vezes em menos de X dias (configurável).

Caso exista nova versão:

Atualizar apenas diferenças.

---

# Retry System

Caso uma URL falhe:

Retry 1

↓

Retry 2

↓

Retry 3

↓

Failed

Registrar erro no banco.

---

# Agendamento

Permitir:

Importar imediatamente

ou

Agendar

Exemplo:

Todo domingo às 03:00

Todo dia às 01:00

Primeiro dia do mês

---

# Integração

Após finalizar uma importação:

Atualizar automaticamente:

Assets

Skills

Design Systems

Prompt Templates

Animation Library

Motion Library

Themes

Masterpieces

Embeddings

Component Library

Knowledge Base

ChromaDB

---

# Dashboard

Adicionar uma página:

Knowledge Dashboard

Widgets:

Websites analisados

Masterpieces

Assets

Skills

Design Systems

Componentes

Embeddings

Tempo médio de análise

Falhas

Última sincronização

---

# Objetivo Final

Permitir que o usuário simplesmente selecione um arquivo contendo centenas ou milhares de URLs e deixe toda a plataforma trabalhar automaticamente.

O sistema será responsável por:

• Validar URLs
• Organizar filas
• Executar Playwright
• Extrair HTML
• Extrair Assets
• Extrair Motion
• Gerar Design Systems
• Gerar Skills
• Atualizar Masterpieces
• Gerar Embeddings
• Atualizar ChromaDB
• Expandir continuamente sua base de conhecimento

📁 Premium Fashion

- Elara
- NoirFrame
- Gucci
- Prada
- Balenciaga

📁 SaaS

- Linear
- Vercel
- Supabase
- Stripe
- Clerk

📁 Awwwards Winners 2025

- 50 URLs

📁 Aura Templates

- Todos os templates do Aura

📁 Meu Dataset

- Lista personalizada

# Frontend — Website Import Center (Premium Experience)

## Objetivo

O Website Import Center não deve parecer apenas uma tela de upload.

Ele deve transmitir a sensação de estar treinando e expandindo a inteligência da plataforma.

A experiência deve ser semelhante a produtos como:

- Linear
- Vercel
- Supabase
- GitHub
- Cursor
- Raycast
- OpenAI Platform

Toda a interface deve ser construída utilizando Shadcn/UI, TailwindCSS, Framer Motion (Motion), Lucide Icons e componentes reutilizáveis.

---

# Layout Geral

A página será dividida em quatro áreas principais.

```

┌──────────────────────────────────────────────────────────────┐

Knowledge Import Center

Treine continuamente sua IA adicionando novas referências.

└──────────────────────────────────────────────────────────────┘

┌──────────────┬───────────────────────────────────────────────┐
│ Sidebar │ Workspace │
│ │ │
│ │ Upload │
│ │ Queue │
│ │ Dashboard │
│ │ History │
│ │ Analytics │
│ │ │
└──────────────┴───────────────────────────────────────────────┘

```

---

# Hero

Adicionar um Hero elegante.

Exemplo:

Knowledge Import Center

Continuously expand your AI knowledge base by importing premium websites, assets and design references.

Botões:

[ Upload URLs ]

[ Analyze Single Website ]

[ Import Dataset ]

---

# Cards de Estatísticas

Logo abaixo do Hero.

```

Websites
12.842

Masterpieces
84

Components
48.932

Assets
19.481

Design Systems
512

Skills
194

Embeddings
125.000

Knowledge Growth
+312 Today

```

Atualização em tempo real via WebSocket.

---

# Upload Area

Criar um grande componente Drag & Drop.

```

┌────────────────────────────────────────────┐

⬆️

Drop TXT, CSV or JSON here

or

[ Select File ]

Accepted:

TXT

CSV

JSON

────────────────────────────────────────────

Auto Validation

Duplicate Detection

Estimated URLs

Import Preview

└────────────────────────────────────────────┘

```

Após selecionar um arquivo:

Mostrar Preview.

Exemplo:

```

Dataset Preview

──────────────────────────────

Filename

premium_fashion.txt

URLs

84

Duplicates

2

Invalid

1

Estimated Time

18 min

Masterpieces

12

```

---

# Import Options

Exibir em Cards.

✓ Generate Design Systems

✓ Extract Components

✓ Extract Assets

✓ Analyze Motion

✓ Generate Skills

✓ Generate Prompt Templates

✓ Generate Embeddings

✓ Save to ChromaDB

✓ Promote to Masterpiece

✓ Rebuild Component Library

Cada opção deverá conter:

Ícone

Descrição

Tooltip

---

# Queue Dashboard

Painel em tempo real.

```

Import Queue

Running

████████░░░░░░

58%

Site:

https://linear.app

Current Stage

Playwright

Elapsed

03:12

Remaining

08:54

```

Cada Job deverá possuir:

Status

Progress

Logs

Botão Cancel

Botão Retry

Botão Details

---

# Pipeline Visualization

Adicionar uma Timeline animada.

```

URL

↓

Playwright

↓

HTML

↓

Assets

↓

Motion

↓

Knowledge Builder

↓

Embeddings

↓

ChromaDB

↓

Finished

```

Cada etapa:

Cinza → aguardando

Azul → executando

Verde → concluída

Vermelho → erro

---

# Live Logs

Adicionar um Terminal.

```

[13:22]

Loading URL...

[13:22]

Capturing screenshots...

[13:23]

Extracting assets...

[13:24]

Generating Design System...

[13:25]

Creating embeddings...

[13:26]

Updating ChromaDB...

```

Pesquisar logs.

Filtrar.

Exportar.

---

# Analytics

Adicionar gráficos.

Importações por dia

Componentes gerados

Assets encontrados

Masterpieces

Tempo médio

Erros

Utilizar Recharts.

---

# History

Tabela Premium.

Arquivo

Data

Quantidade

Status

Tempo

Masterpieces

Botão Reprocess

Botão Download

Botão Delete

---

# Knowledge Explorer

Após finalizar uma importação:

Permitir navegar pelo conhecimento.

```

Knowledge

▼ Masterpieces

▼ Design Systems

▼ Skills

▼ Components

▼ Assets

▼ Themes

▼ Prompt Templates

▼ Motion Library

```

---

# Website Details

Ao clicar em um website.

Mostrar:

Screenshot

Score

Paleta

Tipografia

Assets

Componentes

Animações

Dependências

Prompt Template

Design System

Skill

Masterpiece Score

---

# Masterpiece Badge

Caso o site seja promovido.

Mostrar:

⭐ MASTERPIECE

Cor:

Dourado.

---

# Visual Effects

Utilizar:

Motion

Glassmorphism

Hover Animations

Cards Elevation

Skeleton Loading

Smooth Transitions

Blur Effects

Gradient Borders

Animated Progress

Toast Notifications

---

# Tema

Tema escuro.

Inspirado em:

- Linear
- Vercel
- GitHub Dark
- Cursor

---

# UX

Toda ação deverá possuir feedback visual.

Exemplo:

Upload

↓

Loading

↓

Validation

↓

Queue

↓

Running

↓

Success Animation

↓

Knowledge Updated

---

# Objetivo Final

O usuário deve sentir que está expandindo continuamente a inteligência da plataforma.

O Website Import Center deve funcionar como um verdadeiro centro de treinamento da IA, fornecendo uma experiência premium, moderna e extremamente intuitiva, compatível com aplicações SaaS de alto nível.

Em vez de chamar essa área apenas de "Website Import Center", eu renomearia para Knowledge Hub.

Dentro dele haveria vários módulos:

🧠 Knowledge Hub

├── Import Websites
├── Masterpieces
├── Design Systems
├── Skills
├── Components
├── Assets
├── Motion Library
├── Prompt Templates
├── Knowledge Explorer
├── Analytics
├── Import History
├── Queue Manager
└── Settings