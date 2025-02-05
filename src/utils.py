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


import yfinance as yf

def get_stock_prices():
    """
    Получает текущие цены акций из Yahoo Finance API.
    """
    settings = load_json("user_settings.json")
    user_stocks = settings.get("user_stocks", ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])

    stock_data = {}
    for stock in user_stocks:
        try:
            print(f"Запрос к Yahoo Finance для: {stock}")
            ticker = yf.Ticker(stock)
            stock_info = ticker.history(period="1d")  # Получаем данные за последний день
            if not stock_info.empty:
                stock_data[stock] = stock_info['Close'][0]  # Цена закрытия акции
            else:
                stock_data[stock] = "Нет данных"
        except Exception as e:
            print(f"Ошибка запроса к Yahoo Finance для {stock}: {e}")
            stock_data[stock] = "Ошибка при запросе"

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