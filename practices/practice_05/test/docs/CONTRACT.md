# CONTRACT: UI ↔ Backend

## 1. Данные (модели)
- MenuItem: { id: number, name: string, description?: string, category: 'coffee'|'tea'|'dessert'|string, ingredients: string[], sizes: string[], priceCoffeeCoin: number, prices?: Record<string, number>, calories: number, popularity: number }
- NewsItem: { id: number, title: string, body: string, createdAt: string (ISO8601) }
- OrderItem: { menuId: number, quantity: number }
- Order: { id: number, items: OrderItem[], totalCoffeeCoin: number, discountPercent: number, status: 'created'|'paid', customerId?: string }
- StoreHours: { open: 'HH:MM:SS', close: 'HH:MM:SS' }
- Loyalty: { customerId: string, points: number }
- Review: { id: number, menuId: number, rating: 1..5, comment: string, createdAt: string (ISO8601) }

## 2. Вызовы (эндпоинты)
- Admin (/api/v1/*):
  - GET/POST/GET{id}/PUT{id}/DELETE{id} /menu, GET /menu/{id}/details
  - GET/POST /news
  - GET /status/open?now=, GET /status/hours
  - GET /discounts/current
  - POST /orders, GET /orders/{id}, POST /orders/{id}/pay
  - GET /loyalty/{customerId}
  - GET/POST /reviews
- Public (/api/*):
  - GET /menu?category=&sort=&q=; GET /menu/{id}; POST /menu
  - GET /news, GET /news/{id}
  - GET /store/status
  - GET /discounts/

## 3. Ошибки (формат)
- Унифицированный формат ошибки: { "detail": string }
- Коды: 400 (некорректный ввод), 404 (не найдено), 409 (конфликт — не используется в текущей итерации)
- Сообщения:
  - "Позиция меню не найдена"
  - "Недопустимый menuId"
  - "Заказ не найден"
  - "Новость не найдена"

## 4. Состояния (UI)
- Общие: loading / empty / error / success
- Заказ: status: 'created' → после оплаты 'paid'
- Магазин: { open: boolean }, публичный статус: { open: boolean, next_change: ISO8601 }
- Скидки: { percent: number } (deterministic daily), витрина: [daily, happy_hour, loyalty]

## 5. Версионирование и алиасы
- Admin API под /api/v1/*; публичные алиасы под /api/* для витрины. Приоритет — соответствие фактам кода.
