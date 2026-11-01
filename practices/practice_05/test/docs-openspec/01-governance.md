# Правила (OpenSpec)

## Процесс (SDD OpenSpec)
- Каждая фича оформляется как change под `openspec/changes/<feature>/` с Why/How/What follows
- Последовательность: proposal → design → specs → tasks → implement → archive
- Спеки валидируются перед реализацией; изменения минимальны

## Роли
- Customer: просматривает меню/скидки/новости, создаёт заказы, отзывы
- Barista: операционные действия (в этой итерации не выделены отдельными эндпоинтами)
- Admin: управляет меню/новостями (через админские роуты /api/v1/*)

## Требования к тестам и бенчмаркам
- Pytest: позитивные/негативные/граничные сценарии
- Бенчмарки: ключевые пути GET /api/v1/menu, GET /api/v1/discounts/current, POST /api/v1/orders

## Оглавление ветки
- 00-overview, 01-governance, 02-architecture, 03-product-description
- backend/* и frontend/* артефакты
