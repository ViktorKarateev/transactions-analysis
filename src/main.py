import os
import json
import pandas as pd
from datetime import datetime
from src.utils import get_greeting, get_currency_rates, get_stock_prices
from src.file_readers import load_transactions


def generate_main_page_json(transactions: pd.DataFrame, date_str: str) -> dict:
    """
    Генерирует JSON-ответ для главной страницы.

    :param transactions: DataFrame с транзакциями.
    :param date_str: Строка с датой в формате 'YYYY-MM-DD'.
    :return: Словарь с JSON-ответом.
    """
    try:
        current_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return {"error": "Неверный формат даты. Используйте YYYY-MM-DD."}

    start_date = current_date.replace(day=1)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y", errors="coerce")
    transactions["Сумма операции"] = pd.to_numeric(transactions["Сумма операции"], errors="coerce")

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

    filtered_transactions.loc[:, "Сумма операции"] = pd.to_numeric(filtered_transactions["Сумма операции"],
                                                                   errors="coerce")
    top_transactions = (
        filtered_transactions.nlargest(5, "Сумма операции")
        [["Дата операции", "Сумма операции", "Категория", "Описание"]]
        .to_dict(orient="records")
    )

    # Преобразуем Timestamp в строки
    for transaction in top_transactions:
        transaction["Дата операции"] = transaction["Дата операции"].strftime('%Y-%m-%d')

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


def main():
    print(get_greeting())  # Печатаем приветствие
    while True:
        # Запрашиваем дату для анализа
        date_str = input("Введите дату в формате 'YYYY-MM-DD': ")

        # Проверяем формат даты
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            break  # Если формат даты корректный, выходим из цикла
        except ValueError:
            print("Неверный формат даты. Используйте YYYY-MM-DD.")

    # Загрузка транзакций из Excel-файла
    transactions = load_transactions("data/operations.xlsx")

    if transactions.empty:
        print("Ошибка: не удалось загрузить транзакции.")
        return

    # Генерация отчета
    json_response = generate_main_page_json(transactions, date_str)

    # Пример вывода результата
    print(json.dumps(json_response, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
