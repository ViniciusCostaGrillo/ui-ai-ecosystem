# 🌌 Guia de Instalação e Inicialização: Helix UI

Este tutorial detalha o passo a passo completo para instalar, configurar e rodar o **Helix UI** localmente no seu desktop.

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de que os seguintes componentes estão instalados na sua máquina:

1. **Git** — [Download Git](https://git-scm.com/)
2. **Python 3.12** — [Download Python 3.12](https://www.python.org/downloads/) (marque a opção *"Add Python to PATH"* durante a instalação).
3. **Node.js (v20+ LTS)** — [Download Node.js](https://nodejs.org/)
4. **Ollama** — [Download Ollama](https://ollama.com/) (para rodar os modelos locais de IA sem custos de API).

---

## 🚀 Passo a Passo de Instalação

### Passo 1: Clonar o Repositório
Abra o **PowerShell** ou **Git Bash** e clone o repositório do projeto:
```bash
git clone https://github.com/ViniciusCostaGrillo/Helix-LLM-UI.git
cd Helix-LLM-UI
```

---

### Passo 2: Configurar o Backend (Python)

1. **Criar o ambiente virtual (Virtualenv)** na raiz do projeto:
   ```powershell
   python -m venv .venv
   ```
2. **Ativar o ambiente virtual**:
   * No **PowerShell**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   * No **CMD** ou **Git Bash**:
     ```bash
     source .venv/Scripts/activate
     ```
3. **Instalar as dependências do Backend**:
   ```powershell
   pip install -r backend/requirements.txt
   ```
4. **Instalar os navegadores headless do Playwright** (necessários para os crawlers):
   ```powershell
   playwright install
   ```

---

### Passo 3: Configurar o Frontend (Next.js)

1. Navegar para a pasta do frontend:
   ```powershell
   cd frontend
   ```
2. Instalar as dependências do Node.js:
   ```powershell
   npm install
   ```
3. Retornar para a raiz do projeto:
   ```powershell
   cd ..
   ```

---

### Passo 4: Configurar as Variáveis de Ambiente (`.env`)

1. Crie um arquivo chamado `.env` na raiz do projeto (`Helix-LLM-UI/.env`).
2. Adicione as seguintes configurações padrão para rodar localmente com SQLite e Ollama:
   ```env
   # Bancos de Dados SQLite Locais (Sharding Ativo)
   DATABASE_URL="sqlite:///./test.db"
   ANALYTICS_DATABASE_URL="sqlite:///./test_analytics.db"

   # Integração com Modelos de IA Locais via Ollama (Compatível com OpenAI)
   OPENAI_API_KEY="ollama"
   OPENAI_API_BASE="http://localhost:11434/v1"
   OPENAI_MODEL_NAME="qwen2.5-coder:7b"
   ```

---

### Passo 5: Inicializar o Ollama e Baixar o Modelo

1. Abra o aplicativo desktop do **Ollama** (ele deve aparecer na barra de tarefas do Windows).
2. Abra o terminal e faça o download do modelo recomendado (*Qwen 2.5 Coder 7B*):
   ```powershell
   ollama pull qwen2.5-coder:7b
   ```
3. Teste o modelo local no terminal para verificar se ele está ativo:
   ```powershell
   ollama run qwen2.5-coder:7b "Olá! Você é o gerador de componentes local do Helix UI?"
   ```

---

## 🛠️ Como Iniciar e Rodar a Aplicação

Para iniciar o ecossistema completo integrado, você precisará de **3 terminais** abertos com o ambiente virtual `.venv` ativo:

### Terminal 1: Servidor API Backend (FastAPI)
Inicia o servidor FastAPI local na porta `8000`:
```powershell
$env:DATABASE_URL="sqlite:///./test.db"; $env:PYTHONPATH="."; .venv\Scripts\python.exe -m uvicorn backend.api.main:app --reload --port 8000
```

### Terminal 2: Watchdog de Ingestão de Conhecimento (Knowledge Watchdog)
Inicia o monitor de pastas em tempo real. Qualquer arquivo arrastado para `knowledge_input/` será detectado, processado, extraído e indexado semanticamente:
```powershell
$env:DATABASE_URL="sqlite:///./test.db"; $env:PYTHONPATH="."; .venv\Scripts\python.exe -c "from backend.knowledge.watchdog import KnowledgeWatchdog; import time; w = KnowledgeWatchdog(); w.start(); print('Watchdog ativo monitorando a pasta knowledge_input/... Pressione Ctrl+C para sair'); [time.sleep(1) for _ in iter(int, 1)]"
```

### Terminal 3: Dashboard Frontend (Next.js)
Inicia o servidor de desenvolvimento do frontend:
```powershell
cd frontend
npm run dev
```

Acesse a interface visual do Helix UI no seu navegador: **`http://localhost:3000`**

---

## 🧪 Verificação do Sistema (Executando Testes)

Você pode verificar se todo o sistema está operando corretamente executando o script principal de testes de integração:
```powershell
$env:PYTHONPATH="."; .venv\Scripts\python.exe backend/utils/run_all_tests.py
```
O console exibirá um relatório listando o status de todas as suítes de testes.

---

## 📂 Diretórios Monitorados para Ingestão (`knowledge_input/`)

Arraste os arquivos para as pastas abaixo para que o Watchdog as indexe no ChromaDB automaticamente:
* `.tsx`, `.jsx`, `.ts`, `.js` ➔ `knowledge_input/components/`
* `.yaml`, `.json` de temas ➔ `knowledge_input/design_systems/`
* `.yaml` de regras de prompts ➔ `knowledge_input/skills/`
* `.png`, `.jpg`, `.jpeg`, `.svg` ➔ `knowledge_input/images/`
* `.mp4`, `.webm` ➔ `knowledge_input/videos/`
* `.glb`, `.gltf` ➔ `knowledge_input/3d/`
* `.txt` com links ou referências ➔ `knowledge_input/references/`
