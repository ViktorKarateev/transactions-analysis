import json
import os
import pandas as pd
from typing import Dict, Any, TextIO

def save_to_json(data: Dict[str, Any], filename: str, folder: str = "export") -> None:
    """Сохраняет данные в JSON-файл."""
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)

    with open(file_path, "w", encoding="utf-8") as file:  # type: TextIO
        json.dump(data, file, ensure_ascii=False, indent=4)  # type: ignore

def save_to_excel(data: dict, filename: str, folder: str = "export"):
    """Сохраняет данные в Excel."""
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)
    df = pd.DataFrame(list(data.items()), columns=["Категория", "Сумма"])
    df.to_excel(file_path, index=False)
    print(f"Данные сохранены в {file_path}")

def save_to_csv(data: dict, filename: str, folder: str = "export"):
    """Сохраняет данные в CSV."""
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)
    df = pd.DataFrame(list(data.items()), columns=["Категория", "Сумма"])
    df.to_csv(file_path, index=False, encoding="utf-8")
    print(f"Данные сохранены в {file_path}")
