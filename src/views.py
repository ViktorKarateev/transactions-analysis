import json
import os
import pandas as pd
from datetime import datetime
from typing import Dict, Any


from src.utils import get_greeting, get_currency_rates, get_stock_prices


def generate_main_page_json(transactions: pd.DataFrame, date_str: str) -> Dict[str, Any]:
    """
    Генерирует JSON-ответ для главной страницы.

    :param transactions: DataFrame с транзакциями.
    :param date_str: Строка с датой в формате 'YYYY-MM-DD HH:MM:SS'.
    :return: Словарь с JSON-ответом.
    """
    try:
        current_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return {"error": "Неверный формат даты. Используйте YYYY-MM-DD HH:MM:SS."}

    start_date = current_date.replace(day=1)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], errors="coerce")
    filtered_transactions = transactions[
        (transactions["Дата операции"] >= start_date) &
        (transactions["Дата операции"] <= current_date)
    ]

    cards_summary = (
        filtered_transactions.groupby("Номер карты")["Сумма операции"]
        .sum()
        .reset_index()
    )
    cards_summary["cashback"] = (cards_summary["Сумма операции"].abs() * 0.01).round(2)

    cards_info = cards_summary.to_dict(orient="records")

    top_transactions = (
        filtered_transactions.nlargest(5, "Сумма операции")
        [["Дата операции", "Сумма операции", "Категория", "Описание"]]
        .to_dict(orient="records")
    )

    currency_rates = get_currency_rates() or {}
    stock_prices = get_stock_prices() or {}

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

    with open(file_path, "w", encoding="utf-8") as file:  # type: ignore
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
