import json
import os
import pytest
from unittest.mock import patch, mock_open
from datetime import datetime
from src.utils import load_json, save_json, get_currency_rates, get_stock_prices, get_greeting


@pytest.fixture
def sample_json():
    """Тестовые данные для JSON-файла."""
    return {"key": "value", "test": 123}


def test_load_json(sample_json):
    """Тест загрузки JSON-файла."""
    with patch("builtins.open", mock_open(read_data=json.dumps(sample_json))), \
         patch("os.path.exists", return_value=True):
        data = load_json("fake.json")
        assert data == sample_json


def test_load_json_file_not_found():
    """Тест загрузки JSON, если файл отсутствует."""
    with patch("os.path.exists", return_value=False):
        data = load_json("non_existent.json")
        assert data == {}


def test_save_json(sample_json):
    """Тест сохранения JSON-файла."""
    with patch("builtins.open", mock_open()) as mocked_file:
        save_json(sample_json, "fake.json")
        mocked_file().write.assert_called()


@patch("os.getenv", return_value="test_api_key")
@patch("src.utils.load_json", return_value={"user_currencies": ["USD", "EUR"]})
@patch("src.utils.requests.get")
def test_get_currency_rates(mock_get, mock_load_json, mock_getenv):
    """Тест получения курсов валют с мокированием API."""
    mock_response = {"rates": {"USD": 73.21, "EUR": 87.08}}
    mock_get.return_value.json.return_value = mock_response

    rates = get_currency_rates()
    assert rates == {"USD": 73.21, "EUR": 87.08}


@patch("os.getenv", return_value="test_api_key")
@patch("src.utils.load_json", return_value={"user_stocks": ["AAPL", "TSLA"]})
@patch("src.utils.requests.get")
def test_get_stock_prices(mock_get, mock_load_json, mock_getenv):
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
@patch("src.utils.datetime")
def test_get_greeting(mock_datetime, hour, expected_greeting):
    """Тест определения приветствия по времени."""
    mock_datetime.now.return_value = datetime(2024, 1, 1, hour, 0, 0)
    assert get_greeting() == expected_greeting
