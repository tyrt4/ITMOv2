## Governance (Spec Kit)

### Конституция
- constitution.md определяет:
  - Технологические стандарты (FastAPI, in-memory/SQLite при расширении, pytest/pytest-benchmark)
  - Стандарты тестирования (успех/ошибка/граница + бенчмарки)
  - Соглашения об именовании и границы (работа строго в practices/practice_05/test/)

### SDD-цикл Spec Kit
- Гейты: spec → plan → tasks → implement → review
- Обязательные секции:
  - backend/spec.md: что и почему (истории, FR, AC)
  - backend/plan.md: как (стек, архитектура, эндпоинты, тесты, риски)
  - backend/tasks.md: фазы и критерии done
  - Аналогично для frontend

### Требования к проверкам
- Спеки и планы должны ссылаться на конституцию
- Перед implement — проверка AC и тестов; после implement — зелёные тесты и отсутствие незаполненных разделов
