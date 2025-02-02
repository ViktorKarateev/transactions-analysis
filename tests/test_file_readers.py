import pandas as pd
import pytest
from src.file_readers import load_transactions


@pytest.fixture
def sample_excel(tmp_path):
    """Создаёт временный тестовый Excel-файл с фиктивными данными"""
    test_file = tmp_path / "test.xlsx"
    df = pd.DataFrame({
        "Дата операции": ["2024-01-01", "2024-01-02"],
        "Сумма операции": [100, 200]
    })
    df.to_excel(test_file, index=False)
    return test_file


def test_load_transactions(sample_excel):
    """Тестируем загрузку Excel-файла"""
    df = load_transactions(str(sample_excel))

    assert not df.empty  # Данные должны загружаться
    assert len(df) == 2  # В тестовом файле 2 строки
    assert "Дата операции" in df.columns  # Проверяем, есть ли нужные колонки
    assert "Сумма операции" in df.columns
