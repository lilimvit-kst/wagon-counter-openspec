# Wagon Counter — OpenSpec starter

Новый проект по ТЗ wagon_counter_software_spec_v1_0.md: две камеры 1080p/30, обычный x86 CPU, Edge и центральная платформа.

Подготовлены правила,15 изменений B00–B14,53 требования и 108 сценариев. Прикладной код предстоит написать.

## Начало

Прочитать [подробные правила](docs/OPENSPEC_RULES.md), [порядок](docs/ROADMAP.md), [архитектуру](docs/architecture.md). Требуются Node24.x, Git, Python≥3.9 для инструментов.

```bash
bash scripts/bootstrap_openspec.sh
python3 scripts/check_project.py --can-start B00
bash scripts/with-tools.sh codex
```

В чат Codex:

```text
Используй $openspec-apply-change для b00-contracts-foundation.
Прочитай AGENTS.md и подробные правила. Реализуй и проверь B00,
заполни отчет и verification, заверши локальным коммитом.
```

Первый change уже создан; повторный propose не нужен. Обращение $openspec-apply-change не является Bash-командой. Codex CLI должен быть установлен и авторизован отдельно.

## Состав

| Путь | Назначение |
| --- | --- |
|AGENTS.md|Правила агента и инварианты учета|
|openspec/config.yaml|Контекст, rules артефактов и operations guidance|
|openspec/changes/|Полные планы B00–B14|
|docs/OPENSPEC_RULES.md|Разработка, проверка, запуск инструментов и Git|
|docs/source/|Исходное ТЗ без изменения|
|docs/blocks.json|Граф, сценарии, статусы и доказательства|
|docs/TRACEABILITY.md|Требования → сценарии → ТЗ|
|docs/blocks/|Отчеты, пока planned|
|docs/field-inputs.md|Данные площадки и разрешенные резервные режимы|
|docs/adr/|Архитектурные решения|
|scripts/|Запуск и проверка графа|
|.agents/skills/|Штатные интеграции OpenSpec для Codex|
|.github/workflows/openspec.yml|CI документации и инструментов|

## Проверка

```bash
npm run check
python3 -m unittest discover -s tests/tooling -v
python3 scripts/check_project.py --status
```

Это проверки комплектности планов и структуры доказательств. Реальная приемка счета/камер/ERP выполняется по блокам. Архив включает локальную Git-историю и main; origin не назначен. Подключение нового пустого remote — раздел 12 правил.
