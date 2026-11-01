# Правила (Governance)

Оглавление
- Правила
- Архитектура (docs/ARCHITECTURE.md)
- Описание продукта (docs/PRODUCT_DESCRIPTION.md)
- Контекст продукта (PRODUCT_CONTEXT.md)

Незыблемые правила
- Работа строго внутри practices/practice_05/test/
- SDD через OpenSpec. Каждый change содержит Why / How / What follows
- Тесты и бенчмарки обязательны для ключевых эндпоинтов
- Изменения минимальны и инкрементальны
- Именование и эндпоинты — RESTful; стиль кода — PEP 8, type hints, докстроки для сложных мест

Роли и права
- Customer: оформляет заказы, читает меню, новости, статус
- Barista: видит заказы, помечает оплату (mock)
- Admin: управляет меню и новостями

Стиль коммитов/ветвлений
- Conventional commits при возможности (feat:, fix:, docs:, test:)
- Ссылки на OpenSpec-артефакты под openspec/changes
