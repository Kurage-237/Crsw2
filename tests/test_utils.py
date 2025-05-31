from unittest.mock import MagicMock

import pytest
import requests

from src import utils


def test_extract_existing_urls_normal_case() -> None:
    data = [
        {"url": "http://example.com/1", "title": "dev"},
        {"url": "http://example.com/2", "title": "qa"},
        {"title": "no-url"},
    ]
    result = utils.extract_existing_urls(data)
    assert result == {"http://example.com/1", "http://example.com/2"}


def test_filter_new_vacancies_filters_correctly() -> None:
    existing = {"http://example.com/1", "http://example.com/2"}
    incoming = [{"url": "http://example.com/1"}, {"url": "http://example.com/3"}, {"name": "no-url"}]
    filtered = utils.filter_new_vacancies(incoming, existing)
    assert filtered == [{"url": "http://example.com/3"}, {"name": "no-url"}]  # считается новой


def test_build_hh_api_params_defaults() -> None:
    result = utils.build_hh_api_params("python")
    assert result == {"text": "python", "page": 0, "per_page": 20}


def test_ensure_success_status_passes_on_200() -> None:
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.raise_for_status.return_value = None  # не вызывает исключение
    utils.ensure_success_status(mock_resp)  # не должно выбросить


def test_ensure_success_status_raises_on_error() -> None:
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_resp.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
    with pytest.raises(requests.HTTPError) as excinfo:
        utils.ensure_success_status(mock_resp)
    assert "Ошибка запроса: 500" in str(excinfo.value)
