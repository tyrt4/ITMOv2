# Контекст продукта: Бэкенд кофейни (FastAPI)

## Видение
Построить учебный бэкенд кофейни и минимальный фронтенд, поддерживающие управление меню, новости, заказы и оплату в CoffeeCoin, скидки (happy hour и скидка дня), расписание работы, детали состава/калорий и дополнительные функции (лояльность и отзывы). Доставка — инкрементально через SDD (OpenSpec и Spec Kit).

## Аудитория
- Студенты, практикующие SDD (OpenSpec/Spec Kit)
- Разработчики, добавляющие фичи по спекам, задачам и тестам

## Глоссарий
- CoffeeCoin: внутренняя валюта для цен и оплат
- Menu item: напиток/десерт с названием, составом, размерами, калориями и ценой
- Order: заказ с суммой в CoffeeCoin и статусами created/paid
- Store status: открыт/закрыт из расписания (по умолчанию 08:00–20:00)
- Роли: Customer (делает заказ), Barista (готовит/выдаёт), Admin (управляет меню/новостями)

## Архитектура (высокоуровневая)
- Стек: Python 3 + FastAPI
- Данные: in‑memory (dict/list) на старте; SQLite в перспективе
- API: REST + OpenAPI на `/docs`
- Тесты: `pytest` + `fastapi.testclient` + `pytest-benchmark`
- Запуск: `uvicorn app.main:app --reload`

Обоснование
- FastAPI даёт типизацию, валидацию и OpenAPI из коробки
- In‑memory упрощает сетап; позже можно перейти на SQLite

## Фичи и ссылки
Источник истины — `openspec/changes/*` и код `app/main.py`.
- Foundation (FastAPI): health, ready, `/api`, `/api/v1` — openspec/changes/foundation-fastapi
- Menu management: CRUD меню, details — openspec/changes/menu-management
- News: список и создание — openspec/changes/news
- Orders & Payments: создание, оплата, получение — openspec/changes/orders-payments
- Discounts: скидка дня и happy hour — покрыто в foundation/orders/store-hours
- Store hours: статус и расписание — openspec/changes/store-hours
- Details (composition & calories): `/api/v1/menu/{id}/details` — openspec/changes/details
- Loyalty: баллы по customerId — openspec/changes/loyalty
- Reviews: список/создание — openspec/changes/reviews

Документация
- OpenSpec: каталог `docs-openspec/` (обзор 00–03, backend/frontend артефакты)
- Spec Kit: каталог `docs-speckit/` (constitution, backend/frontend артефакты)
- Сравнение: `COMPARISON.md`
- Общий контракт: `docs/CONTRACT.md` (данные, вызовы, ошибки, состояния)

## Правила и соглашения
- SDD через OpenSpec: каждый change имеет Why / How / What follows
- Независимая ветка Spec Kit с constitution/spec/plan/tasks
- Малые инкрементальные изменения; спеки валидируются до кода
- Тесты покрывают ключевые эндпоинты (успех/ошибка/граница) и бенчмарки
- RESTful стиль, понятные ошибки (`HTTPException(detail)`), публичные алиасы `/api/*` и версии под `/api/v1/*`

## Ссылки быстрого доступа
- API root: GET `/api/v1/` → `{ "service": "coffee-backend", "version": "v1" }`
- Docs: `/docs`
- UI: `/ui/` (если статический фронтенд смонтирован)
