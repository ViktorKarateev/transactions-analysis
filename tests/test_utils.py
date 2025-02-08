import json
import pytest
from unittest.mock import patch, mock_open
from datetime import datetime
from src.utils import load_json, save_json, get_currency_rates, get_stock_prices, get_greeting


@pytest.fixture
def sample_json():
    return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "TSLA"]}


def test_load_json(sample_json):
    with patch("builtins.open", mock_open(read_data=json.dumps(sample_json))), \
         patch("os.path.exists", return_value=True):
        data = load_json("user_settings.json")
        assert data == sample_json


def test_load_json_file_not_found():
    with patch("os.path.exists", return_value=False), \
         patch("builtins.input", side_effect=["USD, EUR", "AAPL, TSLA"]):
        data = load_json("user_settings.json")
        assert data == {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "TSLA"]}


# noinspection PyArgumentList
def test_save_json(sample_json):
    with patch("builtins.open", mock_open()) as mocked_file:
        save_json(sample_json, "user_settings.json")
        mocked_file().write.assert_called()


@patch("requests.get")  # Сначала мокируем requests.get
@patch("os.getenv", return_value="test_api_key")  # Потом os.getenv
def test_get_currency_rates(mock_getenv, mock_get):  # Порядок аргументов должен совпадать!
    mock_response = {"rates": {"USD": 73.21, "EUR": 87.08, "RUB": 97.04}}
    mock_get.return_value.json.return_value = mock_response

    rates = get_currency_rates()
    assert rates == {"USD": 73.21, "EUR": 87.08, "RUB": 97.04}


@patch("requests.get")  # Сначала requests.get
@patch("os.getenv", return_value="test_api_key")  # Потом os.getenv
def test_get_stock_prices(mock_getenv, mock_get):  # Порядок аргументов исправлен
    mock_response = {"AAPL": 150.12, "TSLA": 900.00}
    mock_get.return_value.json.return_value = mock_response

    prices = get_stock_prices(["AAPL", "TSLA"])
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

    # Создаем объект datetime с нужным часом
    mock_now = datetime(2024, 1, 1, hour, 0, 0)

    # Подменяем только вызов datetime.now(), чтобы возвращался объект datetime, а не MagicMock
    mock_datetime.now.return_value = mock_now

    # Проверяем, что get_greeting() вернет правильное приветствие
    assert get_greeting() == expected_greeting