# Decisions and Assumptions

- STACK: Python 3.x + unittest, без внешних зависимостей.
- CHECK_COMMANDS: `bash practices/practice_04/scripts/check.sh`.
- FEATURE_A: добавить опциональный параметр округления для `avg(values, ndigits=None)`.
- FEATURE_B: добавить функцию `median(values)` с обработкой чётных/нечётных длин.
- MCP_TOOL_IDEA: локальный файловый tool `file_summary(path)` — возвращает размер, количество строк и хэш.
- SKILL_IDEA: skill "test-runner" — запуск `scripts/check.sh`, сбор артефактов и сводка.
- CONSTRAINTS: не менять другие практики; не коммитить секреты; не трогать `.env`; БД отсутствует; публичные API — только в пределах practice_04; опираемся на unittest.
