import os
import json
import pandas as pd
import pytest
from unittest.mock import patch, mock_open
from datetime import datetime
from src.views import generate_main_page_json, save_to_json, save_to_excel, save_to_csv


@pytest.fixture
def sample_transactions():
    """Создаёт тестовый DataFrame с транзакциями."""
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


@patch("src.utils.get_currency_rates", return_value={"USD": 73.21, "EUR": 87.08})
@patch("src.utils.get_stock_prices", return_value={"AAPL": 150.12, "TSLA": 900.00})
@patch("src.utils.datetime")
def test_generate_main_page_json(mock_datetime, mock_stocks, mock_currency, sample_transactions):
    """Тест генерации JSON-ответа для главной страницы."""
    test_date = "2024-02-15 12:00:00"

    # Устанавливаем фиксированное время в тесте
    mock_datetime.now.return_value = datetime(2024, 2, 15, 12, 0, 0)

    result = generate_main_page_json(sample_transactions, test_date)

    assert "greeting" in result
    assert "cards" in result
    assert "top_transactions" in result
    assert "currency_rates" in result
    assert "stock_prices" in result
    assert result["greeting"] == "Добрый день"  # Теперь точно "Добрый день"
    assert isinstance(result["cards"], list)
    assert isinstance(result["top_transactions"], list)
    assert isinstance(result["currency_rates"], list)
    assert isinstance(result["stock_prices"], list)


@patch("builtins.open", new_callable=mock_open)
def test_save_to_json(mock_file):
    """Тест сохранения данных в JSON."""
    data = {"test": "value"}
    filename = "test.json"

    save_to_json(data, filename, folder="test_export")

    mock_file.assert_called_once_with(os.path.join("test_export", filename), "w", encoding="utf-8")
    handle = mock_file()
    handle.write.assert_called()


def test_save_to_excel():
    """Тест сохранения данных в Excel."""
    data = {"Категория": 1000, "Продукты": 500}
    filename = "test.xlsx"

    save_to_excel(data, filename, folder="test_export")

    file_path = os.path.join("test_export", filename)
    assert os.path.exists(file_path)
    os.remove(file_path)  # Удаляем тестовый файл


def test_save_to_csv():
    """Тест сохранения данных в CSV."""
    data = {"Категория": 1000, "Продукты": 500}
    filename = "test.csv"

    save_to_csv(data, filename, folder="test_export")

    file_path = os.path.join("test_export", filename)
    assert os.path.exists(file_path)
    os.remove(file_path)  # Удаляем тестовый файл
