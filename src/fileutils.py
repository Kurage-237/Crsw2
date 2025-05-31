import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class VacancyFileHandler(ABC):
    """
    Абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и удаления информации о вакансиях.
    """

    filepath: str

    @abstractmethod
    def __init__(self, filepath: str) -> None:
        pass # pragma: no cover

    # Записать данные о вакансиях в файл
    @abstractmethod
    def write_vacs(self, data: List[Dict[str, Any]], **kwargs: Any) -> None:
        pass # pragma: no cover

    # Загрузить данные о вакансиях из файла
    @abstractmethod
    def load_vacs(self, **kwargs: Any) -> List[Dict[str, Any]]:
        pass # pragma: no cover

    # Удалить информацию о вакансиях из файла
    @abstractmethod
    def clear(self) -> None:
        pass # pragma: no cover


class JSONVacancyFileHandler(VacancyFileHandler):
    """
    Класс, для работы в формате JSON.
    """

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def write_vacs(self, data: List[Dict[str, Any]], **kwargs: Any) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, **kwargs)

    def load_vacs(self, **kwargs: Any) -> Any:
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f, **kwargs)

    def clear(self) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([], f)
