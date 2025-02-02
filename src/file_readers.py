import pandas as pd


def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Загружает транзакции из Excel-файла в DataFrame.

    :param file_path: Путь к файлу .xlsx
    :return: DataFrame с транзакциями
    """
    try:
        df = pd.read_excel(file_path, dtype=str)  # Загружаем всё как строки, чтобы избежать ошибок с типами данных
        return df
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return pd.DataFrame()  # Возвращаем пустой DataFrame, если произошла ошибка
