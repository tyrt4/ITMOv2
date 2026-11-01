## 1. Структура артефактов
- OpenSpec: 00–03 + backend/* + frontend/*, пример: `docs-openspec/backend/specs.md` описывает эндпоинты с AC
- Spec Kit: constitution → backend spec/plan/tasks → frontend spec/plan/tasks, пример: `docs-speckit/backend/plan.md` фиксирует стек и эндпоинты

## 2. Детализация
- OpenSpec даёт Why/How/What follows: `docs-openspec/backend/proposal.md` — разделы ценности/решения/следствий
- Spec Kit разделяет spec (что/почему) и plan (как): `docs-speckit/backend/spec.md` vs `backend/plan.md`

## 3. Роль governance/constitution
- OpenSpec governance: `docs-openspec/01-governance.md` — цикл proposal→design→specs→tasks
- Spec Kit constitution: `docs-speckit/constitution.md` — стандарты стеков/тестов/ограничений

## 4. Review-гейты
- OpenSpec: archive change после tests green; AC в `backend/specs.md`
- Spec Kit: done-criteria в `backend/tasks.md` с фазами

## 5. Формат задач
- OpenSpec: чек-листы в `docs-openspec/backend/tasks.md`
- Spec Kit: фазы и done в `docs-speckit/backend/tasks.md`

## 6. Покрытие бэкенда
- Оба: список эндпоинтов совпадает с кодом. Пример: `GET /api/v1/discounts/current` присутствует в `docs-openspec/backend/specs.md` и `docs-speckit/backend/plan.md`

## 7. Покрытие фронтенда
- Оба: страницы Home/Menu/Item/News/Cart/Checkout/Account/Reviews. Пример: `docs-openspec/frontend/specs.md` и `docs-speckit/frontend/spec.md`

## 8. Удобство использования
- OpenSpec быстрее для feature-by-feature, благодаря Why/How/What follows в одном месте
- Spec Kit удобен для выравнивания терминов и стандартов через constitution и планы

## 9. Вывод
- Использовать обе ветки: OpenSpec для быстрых изменений, Spec Kit для устойчивого процесса и стандартов. Факты согласованы с кодом и tests.
