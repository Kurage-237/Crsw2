import pytest
import requests

from src.API import HeadHunterAPI
from _pytest.monkeypatch import MonkeyPatch
from typing import Any, Dict, List, Optional, Union


class DummyResponse:
    def __init__(self, status_code: int, items: List[Union[Dict[str, int], Any]]):
        self.status_code = status_code
        # Предположим, API возвращает JSON-объект со списком "items"
        self._data = {"items": items}

    def json(self) -> Dict[str, Union[List[Dict[str, int]], List[Any]]]:
        return self._data


def make_dummy_request_fn(page_to_items_map: dict, status_map: Optional[Dict[int, int]]=None) -> object:
    """
    Возвращает функцию для monkeypatch, которая имитирует requests.get.
    - page_to_items_map: dict, где ключ = номер страницы, значение = список items
    - status_map (опционально): dict, где ключ = номер страницы, значение = status_code
    """

    def _dummy_get(url: Any, headers: Any, params: Any) -> object:
        page = params.get("page", 0)
        # Если статус указан вручную — используем его, иначе 200
        status = status_map.get(page, 200) if status_map else 200
        items = page_to_items_map.get(page, [])
        return DummyResponse(status, items)

    return _dummy_get


def test_load_vacancies_accumulates_20_pages(monkeypatch: MonkeyPatch) -> None:
    """
    Проверяем, что HeadHunterAPI.load_vacancies()
    собирает 20 страниц и останавливается, когда page == 20.
    В каждом вызове возвращаем по одному словарю {'id': page}.
    """
    # Для страниц 0..19 возвращаем по одному элементу; для 20 не вызываем, т.к. цикл прекращается
    page_to_items = {i: [{"id": i}] for i in range(20)}
    dummy_fn = make_dummy_request_fn(page_to_items)
    monkeypatch.setattr(requests, "get", dummy_fn)

    api = HeadHunterAPI()
    api.load_vacancies("python")

    # Должно быть ровно 20 элементов: [{"id": 0}, {"id":1}, ..., {"id":19}]
    assert len(api.vacancies) == 20
    # Проверим, что подряд: id 0..19
    ids = [item["id"] for item in api.vacancies]
    assert ids == list(range(20))


def test_load_vacancies_connection_error(monkeypatch: MonkeyPatch) -> None:
    """
    Если первый запрос возвращает статус != 200, ожидаем ConnectionError.
    """
    # Для страницы 0 вернём статус 500
    page_to_items: dict = {0: []}
    status_map = {0: 500}
    dummy_fn = make_dummy_request_fn(page_to_items, status_map=status_map)
    monkeypatch.setattr(requests, "get", dummy_fn)

    api = HeadHunterAPI()
    with pytest.raises(ConnectionError) as excinfo:
        api.load_vacancies("java")
    assert "Ошибка запроса: 500" in str(excinfo.value)


def test_load_vacancies_partial_empty_pages_then_continue(monkeypatch: MonkeyPatch) -> None:
    """
    Проверяем, что если некоторые страницы возвращают пустой список items,
    цикл всё равно идёт до page == 20.
    """
    # Страницы 0..9: по одному элементу; страницы 10..19: [] (пусто)
    page_to_items = {i: [{"id": i}] for i in range(10)}
    for i in range(10, 20):
        page_to_items[i] = []
    dummy_fn = make_dummy_request_fn(page_to_items)
    monkeypatch.setattr(requests, "get", dummy_fn)

    api = HeadHunterAPI()
    api.load_vacancies("c++")

    # Ожидаем: 10 элементов (из 0..9), остальные страницы «пустые» не добавляют
    assert len(api.vacancies) == 10
    ids = [item["id"] for item in api.vacancies]
    assert ids == list(range(10))


def test_load_vacancies_text_parameter_passed(monkeypatch: MonkeyPatch) -> None:
    """
    Проверяем, что параметр 'text' в запросе действительно передаётся в каждый вызов.
    """
    calls = []

    def _capture_get(url: Any, headers: Any, params: Any) -> object:
        calls.append(params.copy())
        # Возвращаем минимальный "пустой" ответ, 20 итераций
        page = params.get("page", 0)
        items = [{"dummy": page}] if page < 1 else []
        return DummyResponse(200, items)

    monkeypatch.setattr(requests, "get", _capture_get)

    api = HeadHunterAPI()
    api.load_vacancies("rust")

    # Проверяем первые два вызова: page=0 с text="rust" и page=1 с text="rust"
    assert calls[0]["text"] == "rust" and calls[0]["page"] == 0
    assert calls[1]["text"] == "rust" and calls[1]["page"] == 1
    # Всего должно быть ровно 20 итераций (page 0..19)
    assert len(calls) == 20
