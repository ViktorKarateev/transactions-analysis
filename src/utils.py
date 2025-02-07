import json
import logging
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from typing import TextIO

# Загружаем переменные окружения из файла .env
load_dotenv()

def load_json(filename: str):
    """
    Загружает JSON-файл и возвращает данные.
    """
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", filename)

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print(f"⚠ Файл {filename} не найден или пуст, запрашиваем данные через API.")
        settings = {
            "user_currencies": request_currencies(),
            "user_stocks": request_stocks()
        }
        save_json(settings, file_path)
        return settings

    try:
        with open(file_path, "r", encoding="utf-8") as file:
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


def request_currencies():
    """
    Запрашивает у пользователя валюты для анализа.
    """
    currencies = input("Введите валюты через запятую (например, USD, EUR): ")
    return [currency.strip() for currency in currencies.split(",")]


def request_stocks():
    """
    Запрашивает у пользователя акции для анализа.
    """
    stocks = input("Введите акции через запятую (например, AAPL, AMZN): ")
    return [stock.strip() for stock in stocks.split(",")]


def get_currency_rates(currency_list=None):
    """ Получение курсов валют через API """
    if currency_list is None:
        currency_list = ["USD", "EUR", "RUB"]  # Валюты по умолчанию
    print(f"Запрашиваем курсы валют для: {currency_list}")

    api_url = "https://api.exchangerate-api.com/v4/latest/USD"  # API для валют
    rates = {}

    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()

        if "rates" in data:
            for currency in currency_list:
                rates[currency] = data["rates"].get(currency, "N/A")  # Если нет валюты, ставим "N/A"
        else:
            print("Ошибка: Нет данных о курсах валют")
            rates = {cur: "N/A" for cur in currency_list}

    except Exception as e:
        print(f"Ошибка получения курсов валют: {e}")
        rates = {cur: "N/A" for cur in currency_list}  # Если ошибка, ставим "N/A"

    return rates


def get_stock_prices(stocks):
    """
    Получает текущие цены акций из Alpha Vantage API.
    """
    api_key = os.getenv("ALPHA_VANTAGE_KEY", "55S27TWDBK01EW51")  # API-ключ
    base_url = "https://www.alphavantage.co/query"
    stock_data = {}

    for stock in stocks:
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": stock,
            "apikey": api_key
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if "Time Series (Daily)" in data:
                last_date = sorted(data["Time Series (Daily)"].keys())[-1]
                stock_data[stock] = float(data["Time Series (Daily)"][last_date]["4. close"])
            else:
                stock_data[stock] = "Ошибка при запросе"
        except requests.RequestException as e:
            stock_data[stock] = "Ошибка при запросе"
            print(f"Ошибка запроса к API для {stock}: {e}")

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
    Настроивает логирование для проекта.
    """
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
