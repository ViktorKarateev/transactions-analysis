import os
import pandas as pd

def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Загружает транзакции из Excel-файла в DataFrame.
    :param file_path: Путь к файлу .xlsx
    :return: DataFrame с транзакциями
    """
    try:
        # Получаем абсолютный путь до файла, относительно корня проекта
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Переходим на уровень выше папки src
        absolute_path = os.path.join(base_dir, file_path)  # Соединяем с папкой data
        print(f"Загружаем файл: {absolute_path}")  # Для отладки

        # Проверяем, существует ли файл
        if not os.path.exists(absolute_path):
            print(f"Файл {absolute_path} не найден!")
            return pd.DataFrame()  # Возвращаем пустой DataFrame, если файл не найден

        df = pd.read_excel(absolute_path, dtype=str)  # Загружаем всё как строки
        return df
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return pd.DataFrame()  # Возвращаем пустой DataFrame, если произошла ошибка

# Пример вызова функции
file_path = 'data/operations.xlsx'  # Путь относительно корня проекта
load_transactions(file_path)
