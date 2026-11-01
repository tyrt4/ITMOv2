# Кофейный бэкенд (FastAPI) — practice_05/test

Что доступно локально
- База приложения: http://localhost:8000/
- Health: GET http://localhost:8000/health → { "status": "ok" }
- Readiness: GET http://localhost:8000/ready → { "ready": true }
- База API (резерв): http://localhost:8000/api
- Корень API v1: GET http://localhost:8000/api/v1/ → { "service": "coffee-backend", "version": "v1" }
- OpenAPI docs: http://localhost:8000/docs
- Frontend UI: http://localhost:8000/ui/ (редирект с "/")

Запуск локально
- Создать venv: `python -m venv .venv && . .venv/bin/activate`
- Установить зависимости: `pip install fastapi uvicorn pytest pytest-benchmark httpx2`
- Старт: `uvicorn app.main:app --reload`

Тесты
- `pytest -q`
Бенчмарки
- `pytest -q -k bench --benchmark-only`

OpenSpec
- `npm exec -y @fission-ai/openspec@latest -- validate --all`

Структура
- app/main.py — FastAPI приложение (health, ready, /api, /api/v1)
- tests/ — pytest тесты
- openspec/ — артефакты OpenSpec
- docs/CONTRACT.md — общий контракт UI↔Backend (данные, вызовы, ошибки, состояния)
