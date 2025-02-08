import os
import json
import pandas as pd
import pytest
from unittest.mock import patch, mock_open
from datetime import datetime
from src.views import generate_main_page_json, save_to_json, save_to_excel, save_to_csv


@pytest.fixture
def sample_transactions():
    """Создает тестовый DataFrame с транзакциями."""
    data = {
        "Дата операции": ["2024-02-01", "2024-02-05", "2024-02-10"],
        "Номер карты": ["1234", "5678", "1234"],
        "Сумма операции": [-500, -200, -300],
        "Категория": ["Продукты", "Развлечения", "Аптека"],
        "Описание": ["Магазин", "Кино", "Аптека"]
    }
    df = pd.DataFrame(data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"])
    return df


@patch("src.views.get_stock_prices")
@patch("src.views.get_currency_rates")
@patch("src.views.get_greeting")
def test_generate_main_page_json(mock_greeting, mock_currency, mock_stocks, sample_transactions):
    """Тест генерации JSON-ответа для главной страницы."""
    # Подготовка тестовых данных
    test_date = "2024-02-15"
    test_stocks = ["AAPL", "TSLA", "GOOGL"]

    # Устанавливаем фиксированные значения для моков
    mock_greeting.return_value = "Добрый день"
    mock_currency.return_value = {"USD": 73.21, "EUR": 87.08}
    mock_stocks.return_value = {
        "AAPL": 227.63,
        "TSLA": 361.62,
        "GOOGL": 185.34
    }

    # Вызываем функцию с передачей списка акций
    result = generate_main_page_json(transactions=sample_transactions, date_str=test_date, stocks=test_stocks)

    # Проверяем, что mock_stocks был вызван с правильными параметрами
    mock_stocks.assert_called_once_with(stocks=test_stocks)

    # Проверяем корректность результата
    assert result["greeting"] == "Добрый день"
    assert isinstance(result["cards"], list)
    assert isinstance(result["top_transactions"], list)
    assert isinstance(result["currency_rates"], list)
    assert isinstance(result["stock_prices"], list)

    # Проверяем данные об акциях
    stock_prices = {item["stock"]: item["price"] for item in result["stock_prices"]}
    assert stock_prices["AAPL"] == 227.63
    assert stock_prices["TSLA"] == 361.62
    assert stock_prices["GOOGL"] == 185.34

    # Проверяем валюты
    currency_rates = {item["currency"]: item["rate"] for item in result["currency_rates"]}
    assert currency_rates["USD"] == 73.21
    assert currency_rates["EUR"] == 87.08

# Пример теста для сохранения в JSON
@patch("builtins.open", new_callable=mock_open)
def test_save_to_json(mock_file):
    """Тест сохранения данных в JSON."""
    data = {"test": "value"}
    filename = "test.json"

    save_to_json(data, filename, folder="test_export")

    mock_file.assert_called_once_with(os.path.join("test_export", filename), "w", encoding="utf-8")
    handle = mock_file()
    handle.write.assert_called()

# Пример теста для сохранения в Excel
def test_save_to_excel():
    """Тест сохранения данных в Excel."""
    data = {"Категория": 1000, "Продукты": 500}
    filename = "test.xlsx"

    save_to_excel(data, filename, folder="test_export")

    file_path = os.path.join("test_export", filename)
    assert os.path.exists(file_path)
    os.remove(file_path)  # Удаляем тестовый файл

# Пример теста для сохранения в CSV
def test_save_to_csv():
    """Тест сохранения данных в CSV."""
    data = {"Категория": 1000, "Продукты": 500}
    filename = "test.csv"

    save_to_csv(data, filename, folder="test_export")

    file_path = os.path.join("test_export", filename)
    assert os.path.exists(file_path)
    os.remove(file_path)  # Удаляем тестовый файл
