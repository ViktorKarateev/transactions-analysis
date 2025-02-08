# Проект для анализа транзакций

Этот проект представляет собой приложение для анализа транзакций из Excel-файлов. Он включает в себя функции для загрузки данных, анализа, создания отчетов и работы с внешними API для получения актуальных данных о курсах валют и ценах акций.

## Структура проекта

1. **`src/`** — основная папка с модулями.
   - **`file_readers.py`** — функции для загрузки данных (например, из Excel, CSV, JSON).
   - **`reports.py`** — функции для анализа транзакций (например, расчет кешбэка, топ-расходов).
   - **`services.py`** — вспомогательные сервисы для расчетов (например, сохранение данных).
   - **`utils.py`** — утилитные функции (например, получение курсов валют и цен акций).
   - **`views.py`** — функции для формирования отчетов в JSON и других форматах.
   - **`main.py`** — основной файл программы для запуска. Здесь организуется вызов всех функций.

2. **`tests/`** — папка с тестами:
   - **`test_file_readers.py`** — тесты для модуля загрузки данных.
   - **`test_reports.py`** — тесты для аналитических функций.
   - **`test_services.py`** — тесты для сервисов.
   - **`test_utils.py`** — тесты для утилит.
   - **`test_views.py`** — тесты для модуля отображения данных (формирование отчетов).

3. **`data/`** — папка для хранения данных (например, Excel-файлы с транзакциями).

4. **`export/`** — папка для сохранения экспортированных отчетов (например, в форматах CSV, Excel, JSON).

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/transactions-analysis.git
   ```

2. Перейдите в папку проекта:
   ```bash
   cd transactions-analysis
   ```

3. Установите зависимости с помощью Poetry:
   ```bash
   poetry install
   ```

## Использование

1. Запустите проект, передав дату в формате `YYYY-MM-DD HH:MM:SS`:
   ```bash
   python -m src.main '2024-02-15 12:00:00'
   ```

   Входной файл с транзакциями по умолчанию должен находиться в папке `data/` и называться `operations.xlsx`. При необходимости измените путь к файлу в коде.

## Основные функции

- **Загрузка транзакций:**
  Модуль `file_readers.py` поддерживает загрузку данных из Excel, CSV и JSON.

- **Анализ транзакций:**
  Модуль `reports.py` анализирует транзакции, рассчитывает кешбэк по категориям, создает топ-расходов.

- **Получение данных из внешних API:**
  Используются API для получения актуальных курсов валют и цен акций. Курсы валют и данные о ценах акций получаются через модули `utils.py`.

- **Формирование отчетов:**
  Модуль `views.py` генерирует отчеты в формате JSON, CSV или Excel.

- **Сервисы:**
  Модуль `services.py` выполняет дополнительные расчеты, например, расчет инвесткопилки, кешбэка и округлений.

## Тестирование

1. Установите зависимости для тестирования:
   ```bash
   poetry add --dev pytest
   ```

2. Для запуска тестов используйте команду:
   ```bash
   poetry run pytest
   ```

   Все тесты должны проходить без ошибок.

## Примечания

- Функции округления (например, для инвесткопилки) позволяют точно контролировать отложенные суммы.
- Для успешной работы с API для акций, необходимо наличие активных интернет-соединений.
- Используйте файл `user_settings.json` для настройки списка отслеживаемых акций.

