import pandas as pd
import json
import numpy as np

def calculate_cashback(transactions: pd.DataFrame, year: int, month: int, cashback_rate: float = 0.01) -> str:
    """
    Вычисляет кешбэк по категориям за указанный месяц.

    :param transactions: DataFrame с транзакциями
    :param year: Год для анализа
    :param month: Месяц для анализа
    :param cashback_rate: Процент кешбэка (по умолчанию 1%)
    :return: JSON-строка с кешбэком по категориям
    """
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], errors="coerce")
    transactions["Сумма операции"] = pd.to_numeric(transactions["Сумма операции"], errors="coerce")

    # Фильтруем только транзакции за нужный месяц и отрицательные (расходы)
    filtered = transactions[
        (transactions["Дата операции"].dt.year == year) &
        (transactions["Дата операции"].dt.month == month) &
        (transactions["Сумма операции"] < 0)
    ]

    # Группируем по категориям и считаем кешбэк
    cashback = (filtered.groupby("Категория")["Сумма операции"]
                .sum()
                .abs() * cashback_rate).round(2)

    return json.dumps(cashback.to_dict(), ensure_ascii=False, indent=4)


def calculate_rounding_savings(transactions: pd.DataFrame, year: int, month: int, rounding_step: int = 50) -> float:
    """
    Рассчитывает сумму, которая могла бы быть отложена в "Инвесткопилку"
    через округление расходов.

    :param transactions: DataFrame с транзакциями (должен содержать 'Дата операции' и 'Сумма операции').
    :param year: Год для анализа.
    :param month: Месяц для анализа.
    :param rounding_step: Шаг округления (10, 50, 100).
    :return: Сумма, которую удалось бы отложить (float).
    """
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], errors="coerce")
    transactions["Сумма операции"] = pd.to_numeric(transactions["Сумма операции"], errors="coerce")

    # Фильтруем только расходы за нужный месяц
    filtered = transactions[
        (transactions["Дата операции"].dt.year == year) &
        (transactions["Дата операции"].dt.month == month) &
        (transactions["Сумма операции"] < 0)
    ].copy()

    # Округляем вверх до ближайшего `rounding_step`
    filtered["Округлённая сумма"] = np.ceil(filtered["Сумма операции"].abs() / rounding_step) * rounding_step
    filtered["В копилку"] = (filtered["Округлённая сумма"] - filtered["Сумма операции"].abs()).astype(float)

    return filtered["В копилку"].sum()
