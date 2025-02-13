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
    """
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%Y-%m-%d", errors="coerce")

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


def get_top_expenses(transactions: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Возвращает топ-N самых больших трат.

    :param transactions: DataFrame с колонками ["Дата операции", "Сумма операции", "Категория", "Описание"]
    :param top_n: Количество записей в топе (по умолчанию 5)
    :return: DataFrame с топ-N тратами
    """
    if "Сумма операции" not in transactions.columns:
        raise ValueError("Отсутствует колонка 'Сумма операции'")

    transactions["Сумма операции"] = pd.to_numeric(transactions["Сумма операции"], errors="coerce")

    # Оставляем только расходы (отрицательные суммы) и сортируем по убыванию
    expenses = transactions[transactions["Сумма операции"] < 0].copy()
    top_expenses = expenses.sort_values(by="Сумма операции", ascending=True).head(top_n)

    return top_expenses[["Дата операции", "Сумма операции", "Категория", "Описание"]]
