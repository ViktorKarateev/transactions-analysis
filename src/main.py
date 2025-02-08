import os
import sys
import json
import pandas as pd
from datetime import datetime
from src.file_readers import load_transactions
from src.reports import get_top_expenses
from src.services import calculate_cashback, calculate_rounding_savings
from src.utils import get_currency_rates, get_stock_prices, load_json, get_greeting
from src.views import save_to_json


def main(input_date: str):
    print("Запуск программы...")

    # Загружаем транзакции
    transactions_file = os.path.join("data", "operations.xlsx")
    print(f"Загружаем файл: {transactions_file}")
    transactions = load_transactions(transactions_file)

    if transactions.empty:
        print("Ошибка: не удалось загрузить транзакции.")
        return

    print(f"Успешно загружено {len(transactions)} транзакций.")

    try:
        current_date = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Ошибка: Некорректный формат даты. Используйте YYYY-MM-DD HH:MM:SS.")
        return

    year, month = current_date.year, current_date.month
    start_date = current_date.replace(day=1)
    print(f"Фильтр данных с {start_date.strftime('%Y-%m-%d')} по {current_date.strftime('%Y-%m-%d')}")

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True, errors="coerce")

    print(f"Диапазон дат в файле: {transactions['Дата операции'].min()} - {transactions['Дата операции'].max()}")

    filtered_transactions = transactions[
        (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= current_date)
    ].copy()

    print(f"Количество транзакций после фильтрации: {len(filtered_transactions)}")

    greeting = get_greeting()
    filtered_transactions["Номер карты"] = filtered_transactions["Номер карты"].fillna("").astype(str)
    filtered_transactions["last_digits"] = filtered_transactions["Номер карты"].apply(lambda x: x[-4:])
    filtered_transactions["Сумма операции"] = pd.to_numeric(filtered_transactions["Сумма операции"], errors="coerce")

    cards_summary = (
        filtered_transactions.groupby("last_digits")["Сумма операции"]
        .sum()
        .reset_index()
    )
    cards_summary["cashback"] = (cards_summary["Сумма операции"].abs() * 0.01).round(2)

    cards_info = cards_summary.to_dict(orient="records")

    top_transactions = get_top_expenses(filtered_transactions).to_dict(orient="records")

    # Получаем курсы валют
    try:
        currency_rates = get_currency_rates()
        if not isinstance(currency_rates, dict):
            raise ValueError("Некорректный формат данных валют")
    except Exception as e:
        print(f"Ошибка получения курсов валют: {e}")
        currency_rates = {"USD": 1, "EUR": 0.96842}

    # Загружаем настройки пользователя
    settings = load_json("user_settings.json")
    stock_symbols = settings.get("user_stocks", ["AAPL", "TSLA", "GOOGL"])

    # Получаем цены акций
    try:
        stock_prices = get_stock_prices(stock_symbols)
        if not isinstance(stock_prices, dict):
            raise ValueError("Некорректный формат данных акций")
        print(f"Ответ API: {stock_prices}")
    except Exception as e:
        print(f"Ошибка получения цен на акции: {e}")
        stock_prices = {symbol: "Ошибка при запросе" for symbol in stock_symbols}

    #  Добавляем вызов сервисов
    cashback_data = calculate_cashback(filtered_transactions, year, month)
    print(f" Кешбэк по категориям: {cashback_data}")

    investment_savings = round(calculate_rounding_savings(filtered_transactions, year, month, 50), 2)
    print(f" Сумма, отложенная в инвесткопилку: {investment_savings}")

    # Вернул правильный `main_page_data`
    main_page_data = {
        "greeting": greeting,
        "cards": cards_info if cards_info else "Нет данных",
        "top_transactions": top_transactions if top_transactions else "Нет транзакций",
        "currency_rates": [{"currency": k, "rate": v} for k, v in currency_rates.items()],
        "stock_prices": [{"stock": k, "price": v} for k, v in stock_prices.items()],
        "cashback": cashback_data,
        "investment_savings": investment_savings
    }

    json_data = json.loads(json.dumps(main_page_data, default=str))

    print(json.dumps(json_data, indent=4, ensure_ascii=False))

    save_to_json(json_data, "main_page.json")
    print("JSON успешно сохранен: main_page.json")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python -m src.main 'YYYY-MM-DD HH:MM:SS'")
    else:
        main(sys.argv[1])
