import json
from pathlib import Path

import pytest

from src.fileutils import JSONVacancyFileHandler


@pytest.fixture
def temp_json_file(tmp_path: Path) -> Path:
    """
    Возвращает путь к временному JSON-файлу.
    """
    return tmp_path / "vacancies_test.json"

def test_init(temp_json_file: Path) -> None:
    assert JSONVacancyFileHandler(str(temp_json_file)).filepath == str(temp_json_file)
    assert JSONVacancyFileHandler().filepath == "data/vacancies.json"

def test_write_and_load_vacs(temp_json_file: Path) -> None:
    """
    Проверяем, что write_vacs() корректно сохраняет список словарей,
    а load_vacs() загружает их.
    """
    handler = JSONVacancyFileHandler(str(temp_json_file))
    data = [
        {
            "name": "Dev1",
            "url": "https://hh.ru/vac1",
            "salary_range": {"currency": "RUR", "from": 100, "to": 200},
            "snippet": {"requirement": "req1"},
        },
        {
            "name": "Dev2",
            "url": "https://hh.ru/vac2",
            "salary_range": {"currency": "USD", "from": 50, "to": 150},
            "snippet": {"requirement": "req2"},
        },
    ]

    # Сохраним данные
    handler.write_vacs(data, indent=2)
    # Проверим, что файл создан и JSON-валиден
    assert temp_json_file.exists()
    loaded_raw = temp_json_file.read_text(encoding="utf-8")
    loaded_json = json.loads(loaded_raw)
    assert loaded_json == data

    # Проверяем load_vacs()
    loaded_from_handler = handler.load_vacs()
    assert isinstance(loaded_from_handler, list)
    assert loaded_from_handler == data


def test_clear_overwrites_with_empty_array(temp_json_file: Path) -> None:
    """
    Проверяем, что clear() перезаписывает файл пустым списком (JSON-массив).
    """
    handler = JSONVacancyFileHandler(str(temp_json_file))
    # Запишем первоначальные данные
    handler.write_vacs([{"foo": "bar"}], indent=0)
    assert temp_json_file.exists()
    assert json.loads(temp_json_file.read_text(encoding="utf-8")) == [{"foo": "bar"}]

    # Очистим
    handler.clear()
    # Файл должен существовать, но содержать пустой JSON-список
    assert temp_json_file.exists()
    loaded = json.loads(temp_json_file.read_text(encoding="utf-8"))
    assert loaded == []


def test_load_vacs_file_not_found(tmp_path: Path) -> None:
    """
    Если файла нет, load_vacs() возбуждает FileNotFoundError.
    """
    non_existent = tmp_path / "does_not_exist.json"
    handler = JSONVacancyFileHandler(str(non_existent))
    with pytest.raises(FileNotFoundError):
        _ = handler.load_vacs()


def test_clear_on_nonexistent_file_creates_empty(temp_json_file: Path) -> None:
    """
    Если файла нет, clear() создает его и пишет пустой список.
    """
    # Убеждаемся, что файла нет
    if temp_json_file.exists():
        temp_json_file.unlink()

    handler = JSONVacancyFileHandler(str(temp_json_file))
    handler.clear()
    assert temp_json_file.exists()
    loaded = json.loads(temp_json_file.read_text(encoding="utf-8"))
    assert loaded == []
