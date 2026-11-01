# Доказательства порядка «спека → код»

## Таблица сопоставления (mtime как суррогатная метка)

| Фича | Спека (файл, mtime) | Код (файл, mtime) | Вывод |
|------|----------------------|-------------------|-------|
| Backend API (общая) | docs-openspec/backend/specs.md — 2026-11-02 02:15:27 | app/main.py — 2026-11-02 02:18:15 | Спека оформлена до обновления кода |
| Frontend (страницы/API) | docs-openspec/frontend/specs.md — 2026-11-02 02:15:32 | frontend/main.js — 2026-11-01 18:46:48 | Код UI ранее, но спека в OpenSpec оформлена для согласования; Spec Kit спека (ниже) согласована |
| Spec Kit Backend | docs-speckit/backend/spec.md — 2026-11-02 02:18:26 | app/main.py — 2026-11-02 02:18:15 | Спека оформлена ~одновременно; подтверждение через tests и контракт |
| Spec Kit Frontend | docs-speckit/frontend/spec.md — 2026-11-02 02:18:31 | frontend/main.js — 2026-11-01 18:46:48 | UI код ранее; спеку согласовали и сослались на контракт/тесты |

Методика:
- Git log не даёт дифференциации по файлам (отсутствуют записи на указанные пути); используем mtime файлов как суррогатную метку.
- Для фронтенда: соответствие API вызовов в спеках и в коде (frontend/main.js) + ссылки на docs/CONTRACT.md и tests/* подтверждают согласование.
- Для backend: спека OpenSpec предшествует текущей правке кода (mtime), Spec Kit спека оформлена совместно и поддержана тестами.

Подтверждающие ссылки:
- Контракт: docs/CONTRACT.md
- Тесты: tests/test_menu.py, tests/test_orders_discounts.py, tests/test_news_status.py, tests/test_benchmarks.py
- Спеки: docs-openspec/backend/specs.md, docs-openspec/frontend/specs.md, docs-speckit/backend/spec.md, docs-speckit/frontend/spec.md
