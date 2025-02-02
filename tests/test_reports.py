import pandas as pd
import pytest
from src.reports import calculate_expenses_by_category


def test_calculate_expenses_by_category():
    """Тестируем подсчёт расходов по категориям"""
    data = {
        "Категория": ["Супермаркеты", "ЖКХ", "Супермаркеты", "Переводы"],
        "Сумма операции": [-1000, -5000, -2000, -3000]
    }
    df = pd.DataFrame(data)

    result = calculate_expenses_by_category(df)

    assert result == {"Супермаркеты": 3000, "ЖКХ": 5000, "Переводы": 3000}
