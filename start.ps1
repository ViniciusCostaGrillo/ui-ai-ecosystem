# ============================================================
# Helix UI - Script de Inicializacao Completo
# ============================================================

param(
    [switch]$ApiOnly,
    [switch]$FrontendOnly,
    [switch]$InitDb
)

$Root = $PSScriptRoot

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "   HELIX UI - Iniciando Servicos...   " -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Inicializar banco de dados SQLite (apenas na primeira vez ou com -InitDb)
if ($InitDb -or -not (Test-Path "$Root\storage\helix.db")) {
    Write-Host "[DB] Inicializando banco de dados SQLite..." -ForegroundColor Yellow
    $env:PYTHONPATH = $Root
    $env:DATABASE_URL = "sqlite:///$Root/storage/helix.db"
    $env:ANALYTICS_DATABASE_URL = "sqlite:///$Root/storage/helix_analytics.db"
    & "$Root\.venv\Scripts\python.exe" backend/utils/init_db.py
    Write-Host "[DB] Banco de dados inicializado!" -ForegroundColor Green
    Write-Host ""
}

# Terminal 1: FastAPI Backend
if (-not $FrontendOnly) {
    Write-Host "[1] Iniciando Backend FastAPI na porta 8000..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:PYTHONPATH='$Root'; `$env:DATABASE_URL='sqlite:///$Root/storage/helix.db'; `$env:ANALYTICS_DATABASE_URL='sqlite:///$Root/storage/helix_analytics.db'; Write-Host 'Backend FastAPI - http://localhost:8000' -ForegroundColor Cyan; Write-Host 'Docs: http://localhost:8000/docs' -ForegroundColor Yellow; & '$Root\.venv\Scripts\python.exe' -m uvicorn backend.api.main:app --reload --port 8000 --host 0.0.0.0" -WindowStyle Normal
    Start-Sleep -Seconds 2
}

# Terminal 2: Knowledge Watchdog
if (-not $ApiOnly -and -not $FrontendOnly) {
    Write-Host "[2] Iniciando Knowledge Watchdog..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:PYTHONPATH='$Root'; `$env:DATABASE_URL='sqlite:///$Root/storage/helix.db'; Write-Host 'Knowledge Watchdog ativo - monitorando knowledge_input/' -ForegroundColor Cyan; & '$Root\.venv\Scripts\python.exe' -c `"from backend.knowledge.watchdog import KnowledgeWatchdog; import time; w = KnowledgeWatchdog(); w.start(); print('Watchdog iniciado!'); [time.sleep(1) for _ in iter(int, 1)]`"" -WindowStyle Normal
    Start-Sleep -Seconds 1
}

# Terminal 3: Next.js Frontend
if (-not $ApiOnly) {
    Write-Host "[3] Iniciando Frontend Next.js na porta 3000..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$Root\frontend'; Write-Host 'Frontend Next.js - http://localhost:3000' -ForegroundColor Cyan; npm run dev" -WindowStyle Normal
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "   Servicos iniciados com sucesso!    " -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Frontend:  http://localhost:3000" -ForegroundColor Yellow
Write-Host "  Backend:   http://localhost:8000" -ForegroundColor Yellow
Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Flags disponiveis:" -ForegroundColor Gray
Write-Host "    .\start.ps1 -InitDb       (re-inicializa o banco de dados)" -ForegroundColor Gray
Write-Host "    .\start.ps1 -ApiOnly      (apenas o backend FastAPI)" -ForegroundColor Gray
Write-Host "    .\start.ps1 -FrontendOnly (apenas o frontend Next.js)" -ForegroundColor Gray
Write-Host ""
