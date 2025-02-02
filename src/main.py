import os
from src.file_readers import load_transactions

# Определяем путь к файлу `operations.xlsx`, чтобы работало на любом компьютере
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Получаем путь к `src/`
FILE_PATH = os.path.join(BASE_DIR, "..", "data", "operations.xlsx")  # Поднимаемся в корень и заходим в `data/`

if __name__ == "__main__":
    transactions = load_transactions(FILE_PATH)

    if transactions.empty:
        print("⚠️ Файл пуст или не найден!")
    else:
        print(transactions.head(10).to_string())  # Выведет данные полностью

