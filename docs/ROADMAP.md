# Порядок B00–B14

Все продуктовые блоки planned. Строгий порядок из ТЗ дополняет зависимости. Первым доступен B00.

| Блок | Change | Зависимости | Результат |
| --- | --- | --- | --- |
| B00 | b00-contracts-foundation | — | Контракты и каркас |
| B01 | b01-reproducible-environment | B00 | Среда, зависимости и CI |
| B02 | b02-local-ledger | B00 B01 | Домен и локальный журнал |
| B03 | b03-edge-control | B02 | Edge API, команды и симулятор |
| B04 | b04-central-sync | B03 | Центр и надежная синхронизация |
| B05 | b05-operator-workspace | B03 B04 | Операторский интерфейс |
| B06 | b06-media-evidence | B01 B04 B05 | Камеры, архив и защищенное видео |
| B07 | b07-validated-models | B06 | Датасет и модель |
| B08 | b08-vision-counting | B02 B03 B07 | CV и счет по видео |
| B09 | b09-wagon-identity | B05 B08 | OCR, двери и ручной режим |
| B10 | b10-visible-fill | B06 B08 | Оценка видимой занятости |
| B11 | b11-engineering-console | B04 B06 B08 B09 B10 | Admin, инциденты и health |
| B12 | b12-business-reporting | B04 B05 B11 | Аналитика и отчеты |
| B13 | b13-erp-delivery | B04 B12 | ERP и редакции результатов |
| B14 | b14-operational-release | B00 B01 B02 B03 B04 B05 B06 B07 B08 B09 B10 B11 B12 B13 | Отказные испытания и выпуск |

Проверка старта: python3 scripts/check_project.py --can-start Bxx. После реальных тестов заполнить verification, завершить задачи, установить verified, архивировать change, повторить проверку. Переход к следующему блоку возможен после архивирования всех предыдущих. Доработка завершенного блока оформляется отдельным change.
