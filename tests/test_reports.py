import pandas as pd
import pytest
from src.reports import calculate_expenses_by_category, filter_transactions, get_top_expenses


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

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%Y-%m-%d")

    filtered = filter_transactions(df, category="Супермаркеты")
    assert len(filtered) == 2

    filtered = filter_transactions(df, start_date="2024-01-02", end_date="2024-01-10")
    assert len(filtered) == 2  # Исправлено с 1 на 2


def test_get_top_expenses():
    """Тестируем выбор Топ-5 трат"""
    data = {
        "Дата операции": ["2024-01-01", "2024-01-05", "2024-01-10", "2024-01-15", "2024-01-20", "2024-01-25"],
        "Сумма операции": [-1000, -5000, -2000, -3000, -8000, -12000],
        "Категория": ["Супермаркеты", "ЖКХ", "Супермаркеты", "Переводы", "Одежда", "Рестораны"],
        "Описание": ["Покупка продуктов", "Оплата коммуналки", "Закупка еды", "Перевод другу", "Новая куртка",
                     "Ужин в ресторане"]
    }
    df = pd.DataFrame(data)

    result = get_top_expenses(df)
    print(result)  # Проверим реальный порядок данных

    assert len(result) == 5
    assert result.iloc[0]["Сумма операции"] == -12000  # Самая большая трата
    assert result.iloc[-1]["Сумма операции"] == -2000  # Последний элемент в топе (меньшая трата)
