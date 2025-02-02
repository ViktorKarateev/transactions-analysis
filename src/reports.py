import pandas as pd
from typing import Optional


def calculate_expenses_by_category(transactions: pd.DataFrame) -> dict:
    """
    Считает общие расходы по каждой категории.

    :param transactions: DataFrame с колонками ["Категория", "Сумма операции"]
    :return: Словарь с суммой расходов по каждой категории
    """
    if "Категория" not in transactions.columns or "Сумма операции" not in transactions.columns:
        raise ValueError("Отсутствуют необходимые колонки: 'Категория' или 'Сумма операции'")

    transactions["Сумма операции"] = pd.to_numeric(transactions["Сумма операции"], errors="coerce")
    expenses = transactions[transactions["Сумма операции"] < 0]

    category_expenses = expenses.groupby("Категория")["Сумма операции"].sum().abs().to_dict()

    return category_expenses


def filter_transactions(
        transactions: pd.DataFrame,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None
) -> pd.DataFrame:
    """
    Фильтрует транзакции по дате, категории и сумме.

    :param transactions: DataFrame с колонками ["Дата операции", "Категория", "Сумма операции"]
    :param start_date: Начальная дата в формате 'YYYY-MM-DD'
    :param end_date: Конечная дата в формате 'YYYY-MM-DD'
    :param category: Фильтрация по категории (например, 'Супермаркеты')
    :param min_amount: Минимальная сумма операции
    :param max_amount: Максимальная сумма операции
    :return: Отфильтрованный DataFrame
    """
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S",
                                                   errors="coerce")

    if start_date:
        transactions = transactions[transactions["Дата операции"] >= pd.to_datetime(start_date)]
    if end_date:
        transactions = transactions[transactions["Дата операции"] <= pd.to_datetime(end_date)]

    if category:
        transactions = transactions[transactions["Категория"] == category]

    transactions["Сумма операции"] = pd.to_numeric(transactions["Сумма операции"], errors="coerce")
    if min_amount is not None:
        transactions = transactions[transactions["Сумма операции"] >= min_amount]
    if max_amount is not None:
        transactions = transactions[transactions["Сумма операции"] <= max_amount]

    return transactions
