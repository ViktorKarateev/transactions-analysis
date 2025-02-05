# Transactions Analysis

## Описание
Программа для анализа транзакций на основе данных из Excel-файла. Она позволяет генерировать отчеты по тратам, кешбэку, инвесткопилке, а также экспортировать результаты в различные форматы (JSON, Excel, CSV).

### Основные функции:
- **Загрузка транзакций**: Программа загружает данные из Excel-файла **`operations.xlsx`**.
- **Генерация отчетов**:
  - Главная страница с данными по тратам, кешбэку и т. д.
  - Кешбэк по категориям.
  - Инвесткопилка.
  - Расходы по категориям.
- **Экспорт данных**: Генерация отчетов в форматах **JSON**, **Excel**, **CSV**.
- **Пользовательский ввод**: Программа запрашивает данные, такие как дата для анализа и шаг округления для инвесткопилки.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your_username/transactions-analysis.git
   cd transactions-analysis
