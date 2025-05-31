from typing import Any, Callable, Dict, List, Optional, Union

import pytest
import requests
from _pytest.monkeypatch import MonkeyPatch

from src.API import HeadHunterAPI


class DummyResponse:
    def __init__(self, status_code: int, items: List[Union[Dict[str, int], Any]]):
        self.status_code = status_code
        self._data = {"items": items}

    def json(self) -> Dict[str, Union[List[Dict[str, int]], List[Any]]]:
        return self._data

    def raise_for_status(self) -> None:
        if not (200 <= self.status_code < 300):
            raise requests.HTTPError(f"Ошибка запроса: {self.status_code}")


def make_dummy_get_fn(page_to_items_map: dict, status_map: Optional[Dict[int, int]] = None) -> Callable:
    """
    Возвращает функцию для monkeypatch, имитирующую requests.Session.get.
    """

    def _dummy_get(self: Any, url: Any, params: Any = None, **kwargs: Any) -> DummyResponse:
        page = params.get("page", 0) if params else 0
        status = status_map.get(page, 200) if status_map else 200
        items = page_to_items_map.get(page, [])
        return DummyResponse(status, items)

    return _dummy_get


def test_load_vacancies_accumulates_20_pages(monkeypatch: MonkeyPatch) -> None:
    page_to_items = {i: [{"id": i}] for i in range(20)}
    dummy_fn = make_dummy_get_fn(page_to_items)
    monkeypatch.setattr(requests.Session, "get", dummy_fn)

    api = HeadHunterAPI()
    api.load_vacancies("python")

    assert len(api.vacancies) == 20
    ids = [item["id"] for item in api.vacancies]
    assert ids == list(range(20))


def test_load_vacancies_connection_error(monkeypatch: MonkeyPatch) -> None:
    page_to_items: dict = {0: []}
    status_map = {0: 500}
    dummy_fn = make_dummy_get_fn(page_to_items, status_map=status_map)
    monkeypatch.setattr(requests.Session, "get", dummy_fn)

    api = HeadHunterAPI()

    with pytest.raises(requests.HTTPError) as excinfo:
        api.load_vacancies("java")

    # Проверим, что это HTTPError с кодом 500
    assert "500" in str(excinfo.value)


def test_load_vacancies_partial_empty_pages_then_continue(monkeypatch: MonkeyPatch) -> None:
    page_to_items = {i: [{"id": i}] for i in range(10)}
    for i in range(10, 20):
        page_to_items[i] = []
    dummy_fn = make_dummy_get_fn(page_to_items)
    monkeypatch.setattr(requests.Session, "get", dummy_fn)

    api = HeadHunterAPI()
    api.load_vacancies("c++")

    assert len(api.vacancies) == 10
    ids = [item["id"] for item in api.vacancies]
    assert ids == list(range(10))


def test_load_vacancies_text_parameter_passed(monkeypatch: MonkeyPatch) -> None:
    calls = []

    def _capture_get(self: Any, url: Any, params: Any = None, **kwargs: Any) -> DummyResponse:
        calls.append(params.copy())
        page = params.get("page", 0) if params else 0
        items = [{"dummy": page}] if page < 1 else []
        return DummyResponse(200, items)

    monkeypatch.setattr(requests.Session, "get", _capture_get)

    api = HeadHunterAPI()
    api.load_vacancies("rust")

    assert calls[0]["text"] == "rust" and calls[0]["page"] == 0
    assert calls[1]["text"] == "rust" and calls[1]["page"] == 1
    assert len(calls) == 20
