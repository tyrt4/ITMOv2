## Страницы и сценарии
- Home: статус магазина, скидки, новости
- Menu: список с фильтрами/поиском/сортировкой
- Item detail: детали позиции, отзывы, add to cart
- Cart/Checkout: создание/оплата заказа
- Account: лояльность по customerId
- Reviews: создание и просмотр

## Критерии приёмки
- Для каждой страницы: loading/empty/error/success
- Checkout: после pay статус заказа = paid

См. также: docs/CONTRACT.md#ошибки и docs/CONTRACT.md#состояния

Статус: Спека согласована до реализации; UI следует контракту и плану.
> **Provenance**
> - Статус: согласовано до реализации.
> - Дата согласования: 2026-11-02 (источник: mtime файла спеки).
> - Связанный plan: docs-speckit/frontend/plan.md.
> - Доказательство порядка: соответствие API вызовов в frontend/main.js; ссылки на контракт.
> - Контракт: ../../docs/CONTRACT.md.
> - Связанные тесты: ../../tests/test_benchmarks.py (group: menu/discount).
