## Данные и модели
- MenuItemIn: name, description, category, ingredients[], sizes[], priceCoffeeCoin, prices{size:price}, calories, popularity
- MenuItem: + id
- NewsItemIn: title, body; NewsItem: + id, createdAt
- OrderItem: menuId, quantity
- OrderIn: items[], customerId?, now?
- Order: id, items[], totalCoffeeCoin, discountPercent, status, customerId?
- ReviewIn: menuId, rating 1–5, comment; Review: + id, createdAt
- StoreHours: open, close (по умолчанию 08:00–20:00)

## Последовательности
1. Создание заказа
   - calc_order_total(items) → discount_of_day + happy_hour_discount(now) → max → totalCoffeeCoin → status=created → save
   - Если customerId, начислить баллы: int(totalCoffeeCoin)
2. Оплата заказа
   - id → статус paid (идемпотентно)

## Обработка ошибок
- 404: меню/заказ/новость не найдены
- 400: Invalid/Недопустимый menuId при заказе/отзыве
- 409: не применимо в текущей итерации

## Границы
- In‑memory хранение; без аутентификации; публичные алиасы только для чтения кроме POST /api/menu (демо)
