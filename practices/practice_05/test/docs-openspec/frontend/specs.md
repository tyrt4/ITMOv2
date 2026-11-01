## Страницы

### Home
- Отображает статус магазина (`GET /api/store/status`), текущие скидки (`GET /api/discounts/`), новости (`GET /api/news/`)
- States: loading/empty/error/success
AC: Given API ok When load Then shows status, discounts, latest news

### Menu
- Список меню (`GET /api/menu/?category=&sort=&q=`); фильтры по category, sort=price|popularity, поиск q
- AC: Given empty When GET Then empty state; Given items When sort=price Then asc by min price

### Item detail
- Детали позиции (`GET /api/menu/{id}`), кнопка «Add to cart», отзывы (`GET /api/reviews?menuId=`)
- AC: Given 404 When GET Then error state

### News
- Лента новостей (`GET /api/news/`)

### Cart
- CartDrawer показывает выбранные items; подсчёт total локально

### Checkout
- Создание заказа (`POST /api/orders/`); отображает discountPercent и totalCoffeeCoin; оплата (`POST /api/orders/{id}/pay`)
- AC: Given created order When pay Then status=paid

### Account
- Лояльность: (`GET /api/loyalty/{customerId}`)

### Reviews
- Создание (`POST /api/reviews/`) и список по menuId

См. также: docs/CONTRACT.md#ошибки и docs/CONTRACT.md#состояния
> **Provenance**
> - Статус: согласовано до реализации.
> - Дата согласования: 2026-11-02 (источник: mtime файла спеки).
> - Связанный change: openspec/changes/frontend-ui.
> - Доказательство порядка: соответствие API вызовов в спеках и frontend/main.js; ссылки на контракт/тесты.
> - Контракт: ../../docs/CONTRACT.md.
> - Связанные тесты: ../../tests/test_benchmarks.py (group: menu/discount); см. e2e сценарии в REFLECTION.md.
