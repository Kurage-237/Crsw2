from abc import ABC, abstractmethod

import requests

from src.vacutils import Vacancy


class ServiceAPI(ABC):
    """
    Абстрактный класс для работы с API сервиса с вакансиями.
    """

    # Запросить список вакансий, включающих ключевое слово.
    @abstractmethod
    def load_vacancies(self, keyword: str) -> None:
        pass # pragma: no cover


class HeadHunterAPI(ServiceAPI):
    """
    Класс для работы с платформой hh.ru.
    """

    # Параметры запроса
    url = "https://api.hh.ru/vacancies"
    headers = {"User-Agent": "HH-User-Agent"}

    def __init__(self) -> None:
        self.params: dict = {"text": "", "page": 0, "per_page": 100}
        self.vacancies: list = []

    def load_vacancies(self, keyword: str) -> None:
        """
        Запросить список вакансий, включающих ключевое слово.
        :param keyword:
        :return:
        """
        self.params["text"] = keyword

        # Список из 20 страниц
        while self.params.get("page") != 20:
            response = requests.get(self.__class__.url, headers=self.__class__.headers, params=self.params)
            if response.status_code != 200:
                raise ConnectionError(f"Ошибка запроса: {response.status_code}")
            vacancies = response.json()["items"]
            self.vacancies.extend(vacancies)
            self.params["page"] += 1
