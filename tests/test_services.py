import pandas as pd
from src.services import calculate_cashback, calculate_rounding_savings


def test_calculate_cashback():
    """Тестируем расчет кешбэка"""
    data = {
        "Дата операции": ["2024-01-05", "2024-01-10", "2024-01-15", "2024-02-01"],
        "Категория": ["Супермаркеты", "ЖКХ", "Супермаркеты", "Переводы"],
        "Сумма операции": [-1000, -5000, -2000, -3000]
    }
    df = pd.DataFrame(data)

    df["Дата операции"] = pd.to_datetime(df["Дата операции"])

    cashback = calculate_cashback(df, 2024, 1, cashback_rate=0.01)

    expected_cashback = {
        "Супермаркеты": 30.0,  # (-1000 - 2000) * 0.01 = 30.0
        "ЖКХ": 50.0  # (-5000) * 0.01 = 50.0
    }

    assert cashback == expected_cashback  # Проверяем, что кешбэк рассчитан правильно


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
