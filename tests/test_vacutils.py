from typing import Optional, Union

import pytest

from src.vacutils import Vacancy


def test_vacancy_salary_none_becomes_zero() -> None:
    """
    Если salary_range=None, то во входе создаётся словарь с from=0, to=0, currency=None.
    """
    vac = Vacancy(name="Test", url="http://example.com", salary_range=None, snippet={"requirement": "req"})
    assert vac.salary_range == {"currency": None, "from": 0, "to": 0}


def test_vacancy_salary_partial_missing_fields() -> None:
    """
    Если salary_range={'currency': 'RUR', 'from': None, 'to': 500},
    то from превратится в 0, to=500.
    """
    raw = {"currency": "RUR", "from": None, "to": 500}
    vac = Vacancy(name="Test", url="http://example.com", salary_range=raw, snippet={})
    assert vac.salary_range == {"currency": "RUR", "from": 0, "to": 500}


def test_vacancy_salary_to_less_than_from_adjusts() -> None:
    """
    Если salary_range={'currency':'USD','from':1000,'to':500},
    то to = from (1000).
    """
    raw = {"currency": "USD", "from": 1000, "to": 500}
    vac = Vacancy(name="TestHighLow", url="http://example.com", salary_range=raw, snippet={})
    assert vac.salary_range["from"] == 1000
    assert vac.salary_range["to"] == 1000


def test_vacancy_comparisons_equal_and_not_equal() -> None:
    """
    Два объекта Vacancy с одинаковым верхним пределом зарплаты считаются равными.
    Иначе not equal.
    """
    vac1 = Vacancy("A", "urlA", {"currency": "RUR", "from": 100, "to": 200}, {})
    vac2 = Vacancy("B", "urlB", {"currency": "USD", "from": 50, "to": 200}, {})
    vac3 = Vacancy("C", "urlC", {"currency": "RUR", "from": 150, "to": 300}, {})

    assert vac1 == vac2
    assert not (vac1 != vac2)
    assert vac1 != vac3
    assert not (vac1 == vac3)


def test_vacancy_comparisons_lt_le_gt_ge() -> None:
    """
    Проверяем __lt__, __le__, __gt__, __ge__ по полю salary_range["to"].
    """
    vac_low = Vacancy("Low", "urlLow", {"currency": "RUR", "from": 100, "to": 150}, {})
    vac_mid = Vacancy("Mid", "urlMid", {"currency": "RUR", "from": 100, "to": 200}, {})
    vac_high = Vacancy("High", "urlHigh", {"currency": "RUR", "from": 200, "to": 300}, {})

    assert vac_low < vac_mid
    assert vac_low <= vac_mid
    assert vac_mid > vac_low
    assert vac_mid >= vac_low

    assert vac_mid < vac_high
    assert vac_mid <= vac_high
    assert vac_high > vac_mid
    assert vac_high >= vac_mid

    # Равные по "to"
    vac_mid2 = Vacancy("Mid2", "urlMid2", {"currency": "RUR", "from": 50, "to": 200}, {})
    assert not (vac_mid < vac_mid2)
    assert vac_mid <= vac_mid2
    assert not (vac_mid > vac_mid2)
    assert vac_mid >= vac_mid2


@pytest.mark.parametrize("other_obj", [123, "string", None, 45.6])
def test_vacancy_comparison_type_error(other_obj: Optional[Union[int, str, float]]) -> None:
    """
    При сравнении Vacancy с не-Vacancy должно возвращаться NotImplemented.
    """
    vac = Vacancy("Name", "url", {"currency": "RUR", "from": 0, "to": 100}, {})  # Проверяем __eq__
    result_eq = vac.__eq__(other_obj)
    assert result_eq is NotImplemented

    result_ne = vac.__ne__(other_obj)
    assert result_ne is NotImplemented

    result_lt = vac.__lt__(other_obj)
    assert result_lt is NotImplemented

    result_le = vac.__le__(other_obj)
    assert result_le is NotImplemented

    result_gt = vac.__gt__(other_obj)
    assert result_gt is NotImplemented

    result_ge = vac.__ge__(other_obj)
    assert result_ge is NotImplemented


def test_vacancy_snippet_fields_preserved() -> None:
    """
    Проверяем, что переданный snippet сохраняется без изменений.
    """
    snippet = {"requirement": "req", "responsibility": "resp"}
    vac = Vacancy("SnipTest", "urlSnip", {"currency": "RUR", "from": 0, "to": 0}, snippet)
    assert vac.snippet == snippet


def validation_errors() -> None:
    snippet = {"requirement": "req", "responsibility": "resp"}
    with pytest.raises(ValueError, match="Значение должно быть непустой строкой."):
        Vacancy(1, "urlSnip", {"currency": "RUR", "from": 0, "to": 0}, snippet)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="Значение должно быть непустой строкой."):
        Vacancy("dsadsa", 2, {"currency": "RUR", "from": 0, "to": 0}, snippet)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="snippet должен быть словарём."):
        Vacancy("fdsdsad", "urlSnip", {"currency": "RUR", "from": 0, "to": 0}, 3)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="snippet должен быть словарём."):
        Vacancy("fdsdsad", "urlSnip", 2, snippet)  # type: ignore[arg-type]
