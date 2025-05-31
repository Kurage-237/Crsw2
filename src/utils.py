from typing import Any, Dict, List, Set

import requests


def extract_existing_urls(vacancies: List[Dict[str, Any]]) -> Set[str]:
    """
    Извлекает множество URL из списка вакансий.
    Игнорирует записи без ключа 'url'.
    """
    return {item["url"] for item in vacancies if "url" in item}


def filter_new_vacancies(data: List[Dict[str, Any]], existing_urls: Set[str]) -> List[Dict[str, Any]]:
    """
    Возвращает только те вакансии, которых нет в existing_urls.
    Если у вакансии нет 'url', она считается новой.
    """
    return [vac for vac in data if vac.get("url") not in existing_urls]


def build_hh_api_params(keyword: str, page: int = 0, per_page: int = 20) -> dict:
    return {"text": keyword, "page": page, "per_page": per_page}


def ensure_success_status(response: Any) -> None:
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise requests.HTTPError(f"Ошибка запроса: {response.status_code}") from e
