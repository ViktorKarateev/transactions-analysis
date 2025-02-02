import pandas as pd


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
