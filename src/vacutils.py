from typing import Any

class Vacancy:
    """
    Класс для работы с вакансиями.
    """

    def __init__(self, name: str, url: str, salary_range: dict | None, snippet: dict):
        # Валидация параметров зарплаты
        if salary_range is None:
            salary_range = {"currency": None, "from": 0, "to": 0}
        else:
            frm = salary_range.get("from")
            to = salary_range.get("to")
            salary_range = {
                "currency": salary_range.get("currency"),
                "from": frm if frm is not None else 0,
                "to": to if to is not None else 0,
            }

        if salary_range["to"] < salary_range["from"]:
            salary_range["to"] = salary_range["from"]

        self.name = name
        self.url = url
        self.salary_range = salary_range
        self.snippet = snippet

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
