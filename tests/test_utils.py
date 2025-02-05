import json
import os
import pytest
from unittest.mock import patch, mock_open
from datetime import datetime
from src.utils import load_json, save_json, get_currency_rates, get_stock_prices, get_greeting


@pytest.fixture
def sample_json():
    """Тестовые данные для JSON-файла."""
    return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "TSLA"]}


def test_load_json(sample_json):
    """Тест загрузки JSON-файла."""
    file_path = os.path.join(os.getcwd(), "user_settings.json")  # Указание правильного пути
    with patch("builtins.open", mock_open(read_data=json.dumps(sample_json))), \
         patch("os.path.exists", return_value=True), \
         patch("os.getcwd", return_value=os.path.dirname(file_path)):  # Подменяем путь на основной каталог проекта
        data = load_json("user_settings.json")
        assert data == sample_json


def test_load_json_file_not_found():
    """Тест загрузки JSON, если файл отсутствует."""
    file_path = os.path.join(os.getcwd(), "user_settings.json")  # Указание правильного пути
    with patch("os.path.exists", return_value=False), \
         patch("builtins.input", side_effect=["USD, EUR", "AAPL, TSLA"]), \
         patch("os.getcwd", return_value=os.path.dirname(file_path)):  # Подменяем путь на основной каталог проекта
        data = load_json("user_settings.json")
        assert data == {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "TSLA"]}


def test_save_json(sample_json):
    """Тест сохранения JSON-файла."""
    file_path = os.path.join(os.getcwd(), "user_settings.json")  # Указание правильного пути
    with patch("builtins.open", mock_open()) as mocked_file, \
         patch("os.getcwd", return_value=os.path.dirname(file_path)):  # Подменяем путь на основной каталог проекта
        save_json(sample_json, "user_settings.json")
        mocked_file().write.assert_called()


@patch("os.getenv", return_value="test_api_key")  # Мокируем getenv
@patch("src.utils.requests.get")  # Мокируем requests.get
def test_get_currency_rates(mock_get, mock_getenv):
    """Тест получения курсов валют с мокированием API."""
    mock_response = {"rates": {"USD": 73.21, "EUR": 87.08}}
    mock_get.return_value.json.return_value = mock_response

    rates = get_currency_rates()
    assert rates == {"USD": 73.21, "EUR": 87.08}


@patch("os.getenv", return_value="test_api_key")  # Мокируем getenv
@patch("src.utils.requests.get")  # Мокируем requests.get
def test_get_stock_prices(mock_get, mock_getenv):
    """Тест получения цен акций с мокированием API."""
    mock_response = {"price": 150.12}
    mock_get.return_value.json.return_value = mock_response

    prices = get_stock_prices()
    assert isinstance(prices, dict)
    assert all(isinstance(v, (float, str)) for v in prices.values())


@pytest.mark.parametrize("hour, expected_greeting", [
    (6, "Доброе утро"),
    (13, "Добрый день"),
    (19, "Добрый вечер"),
    (2, "Доброй ночи"),
])
@patch("src.utils.datetime")  # Мокируем datetime
def test_get_greeting(mock_datetime, hour, expected_greeting):
    """Тест определения приветствия по времени."""
    mock_datetime.now.return_value = datetime(2024, 1, 1, hour, 0, 0)
    assert get_greeting() == expected_greeting
