import pandas as pd
from src.services import calculate_cashback , calculate_rounding_savings
import json


def test_calculate_cashback():
    """Тестируем расчёт кешбэка"""
    data = {
        "Дата операции": ["2024-01-05", "2024-01-10", "2024-01-15"],
        "Категория": ["Супермаркеты", "Рестораны", "Транспорт"],
        "Сумма операции": [-10000, -5000, -2000]
    }
    df = pd.DataFrame(data)

    df["Дата операции"] = pd.to_datetime(df["Дата операции"])

    result = calculate_cashback(df, 2024, 1, cashback_rate=0.01)
    expected = {"Супермаркеты": 100.0, "Рестораны": 50.0, "Транспорт": 20.0}

    assert json.loads(result) == expected


def test_calculate_rounding_savings():
    """Тестируем накопления через округление"""
    data = {
        "Дата операции": ["2024-01-05", "2024-01-10", "2024-01-15"],
        "Сумма операции": [-1712, -457, -982]
    }
    df = pd.DataFrame(data)

    df["Дата операции"] = pd.to_datetime(df["Дата операции"])

    result = calculate_rounding_savings(df, 2024, 1, rounding_step=50)
    expected = 99.0  # (38 + 43 + 8)

    assert result == expected
