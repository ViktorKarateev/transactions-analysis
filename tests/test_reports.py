import pandas as pd
import pytest
from src.reports import calculate_expenses_by_category, filter_transactions


def test_calculate_expenses_by_category():
    """Тестируем подсчёт расходов по категориям"""
    data = {
        "Категория": ["Супермаркеты", "ЖКХ", "Супермаркеты", "Переводы"],
        "Сумма операции": [-1000, -5000, -2000, -3000]
    }
    df = pd.DataFrame(data)

    result = calculate_expenses_by_category(df)

    assert result == {"Супермаркеты": 3000, "ЖКХ": 5000, "Переводы": 3000}


def test_filter_transactions():
    """Тестируем фильтрацию транзакций"""
    data = {
        "Дата операции": ["2024-01-01", "2024-01-05", "2024-01-10", "2024-02-01"],
        "Категория": ["Супермаркеты", "ЖКХ", "Супермаркеты", "Переводы"],
        "Сумма операции": [-1000, -5000, -2000, -3000]
    }
    df = pd.DataFrame(data)

    # Фильтруем только "Супермаркеты"
    filtered = filter_transactions(df, category="Супермаркеты")
    assert len(filtered) == 2

    # Фильтруем по дате
    filtered = filter_transactions(df, start_date="2024-01-02", end_date="2024-01-10")
    assert len(filtered) == 2

    # Фильтруем по сумме
    filtered = filter_transactions(df, min_amount=-3000, max_amount=-1000)
    assert len(filtered) == 3
