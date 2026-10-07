# Recon: Практика 4

Дата: 2026-10-07

Выводы по проекту в рамках каталога `practices/practice_04`:

- В каталоге присутствует только README и презентация, исходного кода и тестов нет.
- В корне репозитория есть `opencode.json` (провайдеры моделей), но hook-ов для автопроверки нет.
- В окружении не гарантированы `pytest`/`ruff`. Для проверок выбрана стандартная библиотека Python: `unittest`.
- CHECK_COMMANDS: `bash practices/practice_04/scripts/check.sh` (внутри исполняет `python -m unittest -q`).

План минимальной реализации:

- Создать минимальный модуль на Python с юнит-тестами (unittest).
- Настроить скрипт `scripts/check.sh` для единой проверки.
- Настроить git hook (pre-commit) и описать интеграцию с OpenCode hook в evidence.
- Реализовать skill и минимальный MCP tool (stdin/stdout JSON-RPC), собрать доказательства запусков.
