## Описание продукта (Spec Kit)

### Видение и аудитория
- Учебная витрина кофейни для демонстрации SDD: Customers, Admins (операции админа — через /api/v1/*), Baristas вне текущего scope UI.

### Ключевые сценарии
- Просмотр меню и деталей (ingredients, calories, prices)
- Создание заказа и оплата (mock), просмотр статуса заказа
- Просмотр скидок (daily/happy hour) и статуса магазина
- Чтение и публикация новостей (Admin)
- Начисление баллов лояльности по customerId
- Добавление отзывов по позициям меню

### Что входит / не входит
- Входит: все сценарии на in-memory данных; публичные алиасы `/api/*`, админские `/api/v1/*`
- Не входит: персистентность БД, аутентификация, внешние платёжные сервисы

### Фирменный стиль
- Палитра: #00704A, #D4E9E2, #F1F8F6, #1E3932
- Типографика: Playfair Display (заголовки) + Inter (текст)

### Глоссарий
- CoffeeCoin — внутренняя валюта; Menu item; Order; Store status; Loyalty points; Review

### Ссылки на спецификации
- Backend: см. `docs-speckit/backend/spec.md` (что/почему) и `backend/plan.md` (как)
- Frontend: см. `docs-speckit/frontend/spec.md` и `frontend/plan.md`
