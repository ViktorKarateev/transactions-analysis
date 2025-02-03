import pandas as pd
import json

def calculate_cashback(transactions: pd.DataFrame, year: int, month: int, cashback_rate: float = 0.01) -> str:
    """
    Вычисляет кешбэк по категориям за указанный месяц.

    :param transactions: DataFrame с транзакциями
    :param year: Год для анализа
    :param month: Месяц для анализа
    :param cashback_rate: Процент кешбэка (по умолчанию 1%)
    :return: JSON-строка с кешбэком по категориям
    """
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], errors="coerce")
    transactions["Сумма операции"] = pd.to_numeric(transactions["Сумма операции"], errors="coerce")

    # Фильтруем только транзакции за нужный месяц и отрицательные (расходы)
    filtered = transactions[
        (transactions["Дата операции"].dt.year == year) &
        (transactions["Дата операции"].dt.month == month) &
        (transactions["Сумма операции"] < 0)
    ]

    # Группируем по категориям и считаем кешбэк
    cashback = (filtered.groupby("Категория")["Сумма операции"]
                .sum()
                .abs() * cashback_rate).round(2)

    return json.dumps(cashback.to_dict(), ensure_ascii=False, indent=4)
