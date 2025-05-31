from abc import ABC, abstractmethod
from typing import Any, Union

import requests

from src import utils


class ServiceAPI(ABC):
    """
    Абстрактный класс для работы с API сервиса с вакансиями.
    """

    # Подключится к API
    @abstractmethod
    def _connect(self) -> dict:
        pass  # pragma: no cover

    # Запросить список вакансий, включающих ключевое слово.
    @abstractmethod
    def load_vacancies(self, keyword: str) -> None:
        pass  # pragma: no cover


class HeadHunterAPI(ServiceAPI):
    """Класс для работы с API hh.ru"""

    __url = "https://api.hh.ru/vacancies"
    __headers = {"User-Agent": "HH-API-Client"}

    def __init__(self) -> None:
        self.__session = requests.Session()
        self.__session.headers.update(self.__headers)
        self.params: dict[str, Union[str, int]] = {"text": "", "page": 0, "per_page": 20}
        self.vacancies: list[dict] = []

    def _connect(self) -> Any:
        response = self.__session.get(self.__url, params=self.params)
        utils.ensure_success_status(response)
        return response.json().get("items", [])

    def load_vacancies(self, keyword: str) -> None:
        self.params["text"] = keyword
        self.vacancies = []
        self.params["page"] = 0

        while int(self.params["page"]) < 20:
            self.vacancies.extend(self._connect())
            self.params["page"] = int(self.params["page"]) + 1
