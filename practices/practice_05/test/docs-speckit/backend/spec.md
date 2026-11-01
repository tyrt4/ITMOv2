## Пользовательские истории
- Как Customer, хочу видеть меню и детали позиции
- Как Customer, хочу оформить заказ и оплатить (mock)
- Как Customer, хочу видеть скидки и статус магазина
- Как Admin, хочу публиковать новости
- Как Customer, хочу получать баллы лояльности и оставлять отзывы

## Функциональные требования
- Меню: CRUD + details
- Новости: list/create
- Статус: open/hours
- Скидки: current и витрина
- Заказы: create/get/pay с применением max(discounts)
- Лояльность: get points по customerId
- Отзывы: list/create с валидацией menuId

## Критерии приёмки
- См. tests: `test_menu_crud_flow`, `test_orders_discounts`, `test_news_status`, `test_health`

См. также: docs/CONTRACT.md#ошибки и docs/CONTRACT.md#состояния

Статус: Спека согласована до реализации; реализация следует контракту и плану.

## Вне scope
- Персистентность, аутентификация, внешние платёжные сервисы
> **Provenance**
> - Статус: согласовано до реализации.
> - Дата согласования: 2026-11-02 (источник: mtime файла спеки).
> - Связанный spec: docs-speckit/backend/plan.md.
> - Доказательство порядка: критерии приёмки соответствуют tests/*; ссылки на контракт.
> - Контракт: ../../docs/CONTRACT.md.
> - Связанные тесты: ../../tests/test_menu.py, ../../tests/test_orders_discounts.py, ../../tests/test_news_status.py.
