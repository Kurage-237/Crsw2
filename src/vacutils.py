from typing import Any

class Vacancy:
    """
    Класс для работы с вакансиями.
    """
    __slots__ = ("name", "url", "salary_range", "snippet")

    def __init__(self, name: str, url: str, salary_range: dict | None, snippet: dict):
        self.name = self.__validate_string(name)
        self.url = self.__validate_string(url)
        self.salary_range = self.__validate_salary_range(salary_range)
        self.snippet = self.__validate_snippet(snippet)

    @staticmethod
    def __validate_salary_range(salary_range: dict | None) -> dict:
        """Валидация и нормализация параметров зарплаты."""
        if salary_range is None:
            return {"currency": None, "from": 0, "to": 0}

        if not isinstance(salary_range, dict):
            raise ValueError("salary_range должен быть словарём или None") # pragma: no cover

        frm = salary_range.get("from") or 0
        to = salary_range.get("to") or 0
        if to < frm:
            to = frm
        return {
            "currency": salary_range.get("currency"),
            "from": frm,
            "to": to,
        }

    @staticmethod
    def __validate_string(value: Any) -> str:
        """Валидация строковых значений (не пустая строка)."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Значение должно быть непустой строкой.") # pragma: no cover
        return value.strip()

    @staticmethod
    def __validate_snippet(snippet: Any) -> dict:
        """Валидация snippet (должен быть словарём)."""
        if not isinstance(snippet, dict):
            raise ValueError("snippet должен быть словарём.") # pragma: no cover
        return snippet

    def __eq__(self, other: object) -> bool | Any:
        if isinstance(other, Vacancy):
            return self.salary_range["to"] == other.salary_range["to"]
        else:
            return NotImplemented

    def __ne__(self, other: object) -> bool | Any:
        if isinstance(other, Vacancy):
            return self.salary_range["to"] != other.salary_range["to"]
        else:
            return NotImplemented

    def __lt__(self, other: object) -> bool | Any:
        if isinstance(other, Vacancy):
            return self.salary_range["to"] < other.salary_range["to"]
        else:
            return NotImplemented

    def __le__(self, other: object) -> bool | Any:
        if isinstance(other, Vacancy):
            return self.salary_range["to"] <= other.salary_range["to"]
        else:
            return NotImplemented

    def __gt__(self, other: object) -> bool | Any:
        if isinstance(other, Vacancy):
            return self.salary_range["to"] > other.salary_range["to"]
        else:
            return NotImplemented

    def __ge__(self, other: object) -> bool | Any:
        if isinstance(other, Vacancy):
            return self.salary_range["to"] >= other.salary_range["to"]
        else:
            return NotImplemented