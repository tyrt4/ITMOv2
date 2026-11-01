## Стек и архитектура
- FastAPI + in‑memory repos; авто OpenAPI
- Слои: routers → helpers → repos

## Эндпоинты
- `/health`, `/ready`, `/api`, `/api/v1/`
- `/api/v1/menu`, `/api/menu`
- `/api/v1/news`, `/api/news`
- `/api/v1/status`, `/api/store/status`
- `/api/v1/discounts`, `/api/discounts`
- `/api/v1/orders`, `/api/orders`
- `/api/v1/loyalty`, `/api/loyalty`
- `/api/v1/reviews`, `/api/reviews`

## Модели и данные
- MenuItem, NewsItem, Order(+items), Review, StoreHours, Loyalty

## Тесты и бенчмарки
- pytest: покрытие ключевых сценариев
- benchmarks: GET menu, GET discounts/current, POST orders

## Риски
- In‑memory потеря данных между рестартами; публичные алиасы позволяют запись (только демо)

## Зависимости
- Основа → меню → детали → новости/статус/скидки → заказы → лояльность → отзывы
