## Технологические стандарты
- Backend: FastAPI, Python 3.x
- Data: in‑memory (dict/list), без внешних БД/сервисов
- Tests: pytest, pytest-benchmark, fastapi.testclient
- Frontend: статический UI или React/Vite (при переносе)

## Стандарты тестирования
- Каждый эндпоинт: успех, ошибка, граница; бенчмарки для ключевых путей
- Команды: `pytest -q`, `pytest -q -k bench --benchmark-only`

## Соглашения об именовании
- Эндпоинты REST под `/api/v1/*` (admin) и публичные алиасы `/api/*`
- Модели: `MenuItem`, `Order`, `NewsItem`, `Review`

## Ограничения
- Работа строго в `practices/practice_05/test/`
- Без внешних БД и сервисов; запуск локально

## Разделение требований
- Backend: реализация REST API согласно spec → plan → tasks
- Frontend: страницы и компоненты, интеграция через публичные `/api/*`
