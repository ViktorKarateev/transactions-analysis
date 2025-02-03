import pytest
import os
import json
import pandas as pd
from src.views import save_to_json, save_to_excel, save_to_csv

@pytest.fixture
def sample_data():
    """Пример данных для тестов."""
    return {"Категория 1": 1000, "Категория 2": 500}

@pytest.fixture
def output_folder():
    """Возвращает путь к папке с экспортированными файлами."""
    return "export"

def test_save_to_json(sample_data, output_folder):
    """Тест сохранения в JSON."""
    filename = "test.json"
    file_path = os.path.join(output_folder, filename)

    save_to_json(sample_data, filename, output_folder)

    # Проверяем, что файл создан
    assert os.path.exists(file_path)

    # Проверяем содержимое файла
    with open(file_path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    assert loaded_data == sample_data

    # Удаляем файл после теста
    os.remove(file_path)

def test_save_to_excel(sample_data, output_folder):
    """Тест сохранения в Excel."""
    filename = "test.xlsx"
    file_path = os.path.join(output_folder, filename)

    save_to_excel(sample_data, filename, output_folder)

    # Проверяем, что файл создан
    assert os.path.exists(file_path)

    # Проверяем содержимое файла
    df = pd.read_excel(file_path)
    assert list(df.columns) == ["Категория", "Сумма"]
    assert df.shape[0] == len(sample_data)

    # Удаляем файл после теста
    os.remove(file_path)

def test_save_to_csv(sample_data, output_folder):
    """Тест сохранения в CSV."""
    filename = "test.csv"
    file_path = os.path.join(output_folder, filename)

    save_to_csv(sample_data, filename, output_folder)

    # Проверяем, что файл создан
    assert os.path.exists(file_path)

    # Проверяем содержимое файла
    df = pd.read_csv(file_path)
    assert list(df.columns) == ["Категория", "Сумма"]
    assert df.shape[0] == len(sample_data)

    # Удаляем файл после теста
    os.remove(file_path)
