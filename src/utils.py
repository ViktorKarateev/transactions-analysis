import json
import logging
import os
from datetime import datetime
import requests
from typing import TextIO


def load_json(filename: str):
    """
    Загружает JSON-файл и возвращает данные.
    """
    if not os.path.exists(filename):
        print(f"⚠ Файл {filename} не найден, загружаем пустые данные.")
        return {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Ошибка при чтении JSON {filename}: {e}")
        return {}


def save_json(data, filename: str):
    """
    Сохраняет данные в JSON-файл.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:  # type: TextIO
            json.dump(data, file, ensure_ascii=False, indent=4)  # type: ignore
    except IOError as e:
        print(f"Ошибка при сохранении файла {filename}: {e}")


def get_currency_rates():
    """
    Получает текущие курсы валют через API и учитывает настройки пользователя.
    """
    settings = load_json("user_settings.json")
    user_currencies = settings.get("user_currencies", ["USD", "EUR"])

    api_key = os.getenv("API_LAYER_KEY")
    if not api_key:
        print("⚠ API ключ не найден. Проверьте .env файл.")
        return None

    url = "https://api.apilayer.com/exchangerates_data/latest?base=USD"
    headers = {"apikey": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        rates = {currency: data["rates"].get(currency, "N/A") for currency in user_currencies}
        return rates
    except requests.RequestException as e:
        print(f"Ошибка запроса к API: {e}")
        return None


def get_stock_prices():
    """
    Получает текущие цены акций S&P 500 из API.
    """
    settings = load_json("user_settings.json")
    user_stocks = settings.get("user_stocks", ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])

    api_key = os.getenv("API_LAYER_KEY")
    if not api_key:
        print("⚠ API ключ не найден. Проверьте .env файл.")
        return None

    stock_data = {}
    for stock in user_stocks:
        url = f"https://api.apilayer.com/market_data/quote?symbol={stock}"
        headers = {"apikey": api_key}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            stock_data[stock] = data.get("price", "N/A")
        except requests.RequestException as e:
            print(f"Ошибка запроса к API для {stock}: {e}")
            stock_data[stock] = "Ошибка"

    return stock_data


def get_greeting():
    """
    Определяет приветствие на основе текущего времени.
    """
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def setup_logging():
    """
    Настраивает логирование для проекта.
    """
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )