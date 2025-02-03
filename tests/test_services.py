import pandas as pd
from src.services import calculate_cashback
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
