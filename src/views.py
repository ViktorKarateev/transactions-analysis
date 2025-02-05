import os
import json
import pandas as pd
from datetime import datetime
from typing import Dict, Any
from src.utils import get_currency_rates, get_stock_prices, get_greeting


def generate_main_page_json(transactions: pd.DataFrame, date_str: str) -> Dict[str, Any]:
    """
    Генерирует JSON-ответ для главной страницы.

    :param transactions: DataFrame с транзакциями.
    :param date_str: Строка с датой в формате 'YYYY-MM-DD'.
    :return: Словарь с JSON-ответом.
    """
    try:
        current_date = datetime.strptime(date_str, "%Y-%m-%d")  # Мы теперь используем только дату без времени
    except ValueError:
        return {"error": "Неверный формат даты. Используйте YYYY-MM-DD."}

    start_date = current_date.replace(day=1)  # Начало месяца

    # Преобразуем все даты в датафрейме в формат без времени
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%Y-%m-%d", errors="coerce")

    # Фильтруем транзакции по диапазону дат
    filtered_transactions = transactions[
        (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= current_date)
        ]

    # Сводка по картам
    cards_summary = (
        filtered_transactions.groupby("Номер карты")["Сумма операции"]
        .sum()
        .reset_index()
    )
    cards_summary["cashback"] = (cards_summary["Сумма операции"].abs() * 0.01).round(2)

    cards_info = cards_summary.to_dict(orient="records")

    # Топ-5 транзакций по сумме
    filtered_transactions["Сумма операции"] = pd.to_numeric(filtered_transactions["Сумма операции"], errors="coerce")
    top_transactions = (
        filtered_transactions.nlargest(5, "Сумма операции")
        [["Дата операции", "Сумма операции", "Категория", "Описание"]]
        .to_dict(orient="records")
    )

    # Получаем курсы валют и цены акций
    currency_rates = get_currency_rates() or {}
    stock_prices = get_stock_prices() or {}

    # Формируем JSON-ответ
    response = {
        "greeting": get_greeting(),  # Приветствие на основе времени
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
