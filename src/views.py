import os
import json
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
from src.utils import get_currency_rates, get_stock_prices, get_greeting


def generate_main_page_json(transactions: pd.DataFrame, date_str: str, stocks: List[str] = None) -> Dict[str, Any]:
    """
    Генерирует JSON-ответ для главной страницы.

    :param transactions: DataFrame с транзакциями.
    :param date_str: Строка с датой в формате 'YYYY-MM-DD'.
    :param stocks: Список акций для отслеживания
    :return: Словарь с JSON-ответом.
    """
    if stocks is None:
        stocks = ["AAPL", "TSLA", "GOOGL"]  # Значения по умолчанию

    try:
        current_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return {"error": "Неверный формат даты. Используйте YYYY-MM-DD."}

    start_date = current_date.replace(day=1)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%Y-%m-%d", errors="coerce")

    filtered_transactions = transactions[
        (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= current_date)
    ]

    cards_summary = (
        filtered_transactions.groupby("Номер карты")["Сумма операции"]
        .sum()
        .reset_index()
    )
    cards_summary["cashback"] = (cards_summary["Сумма операции"].abs() * 0.01).round(2)

    cards_info = cards_summary.to_dict(orient="records")

    filtered_transactions["Сумма операции"] = pd.to_numeric(filtered_transactions["Сумма операции"], errors="coerce")
    top_transactions = (
        filtered_transactions.nlargest(5, "Сумма операции")
        [["Дата операции", "Сумма операции", "Категория", "Описание"]]
        .to_dict(orient="records")
    )

    # Получаем курсы валют
    currency_rates = get_currency_rates()
    if currency_rates is None:
        currency_rates = {}

    # Получаем цены акций
    print(f"Запрашиваем цены акций для: {stocks}")  # Отладочный вывод
    stock_prices = get_stock_prices(stocks=stocks)
    if stock_prices is None:
        stock_prices = {}

    response = {
        "greeting": get_greeting(),
        "cards": cards_info,
        "top_transactions": top_transactions,
        "currency_rates": [{"currency": k, "rate": v} for k, v in currency_rates.items()],
        "stock_prices": [{"stock": k, "price": v} for k, v in stock_prices.items()]
    }

    return response


def save_to_json(data: Dict[str, Any], filename: str, folder: str = "export") -> None:
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)

    with open(file_path, "w", encoding="utf-8") as file:
        # noinspection PyTypeChecker
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_to_excel(data: Dict[str, Any], filename: str, folder: str = "export") -> None:
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)

    df = pd.DataFrame(list(data.items()), columns=["Категория", "Сумма"])
    df.to_excel(file_path, index=False)
    print(f"Данные сохранены в {file_path}")


def save_to_csv(data: Dict[str, Any], filename: str, folder: str = "export") -> None:
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)

    df = pd.DataFrame(list(data.items()), columns=["Категория", "Сумма"])
    df.to_csv(file_path, index=False, encoding="utf-8")
    print(f"Данные сохранены в {file_path}")
