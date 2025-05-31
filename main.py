from src.API import HeadHunterAPI
from src.fileutils import JSONVacancyFileHandler
from src.vacutils import Vacancy


def user_interaction() -> None:
    api = HeadHunterAPI()
    file_handler = JSONVacancyFileHandler("data/vacancies.json")
    vacancies: list[Vacancy] = []

    while True:
        print("\n=== Меню ===")
        print("1) Загрузка вакансий по ключевому слову")
        print("2) Топ-N вакансий по зарплате")
        print("3) Поиск по ключевому слову в описании")
        print("4) Сохранить вакансии в файл")
        print("5) Загрузить вакансии из файла")
        print("6) Удалить данные из файла")
        print("0) Выход")

        choice = input("Выберите пункт: ").strip()
        if choice == "0":
            break

        # 1) Поиск — заполняем vacancies из api.vacancies (список dict)
        if choice == "1":
            kw = input("Ключевое слово для поиска: ").strip()
            api.load_vacancies(kw)  # заполняет api.vacancies
            vacancies = []
            for raw in api.vacancies:
                name = raw["name"]
                url = raw.get("alternate_url", "") or raw.get("url", "")
                # формат salary может быть в raw["salary"] или raw["salary_range"]
                salary_dict = raw.get("salary_range") or raw.get("salary")
                snippet = raw.get("snippet", {})
                vacancies.append(Vacancy(name, url, salary_dict, snippet))
            print(f"Найдено {len(vacancies)} вакансий.")

        # 2) Топ-N по максимальной зарплате
        elif choice == "2":
            if not vacancies:
                print("Сначала выполните поиск (пункт 1).")
                continue
            try:
                n = int(input("Сколько вакансий вывести?: ").strip())
            except ValueError:
                print("Нужно ввести число.")
                continue

            top_n = sorted(vacancies, reverse=True)[:n]
            for v in top_n:
                lo = v.salary_range["from"]
                hi = v.salary_range["to"]
                cur = v.salary_range["currency"]
                print(f"{v.name} — от {lo} до {hi} {cur}")

        # 3) Поиск по ключевому слову в описании
        elif choice == "3":
            if not vacancies:
                print("Нет вакансий (пункт 1).")
                continue
            kw = input("Ключевое слово в описании: ").strip().lower()
            filtered = []
            for v in vacancies:
                # v.snippet — dict
                req = v.snippet.get("requirement", "") or ""
                resp = v.snippet.get("responsibility", "") or ""
                text = (req + " " + resp).lower()
                if kw in text:
                    filtered.append(v)
            print(f"Найдено {len(filtered)} вакансий:")
            for v in filtered:
                print(f"- {v.name} ({v.url})")

        # 4) Сохранить вакансии в файл (только атрибуты Vacancy)
        elif choice == "4":
            if not vacancies:
                print("Нет вакансий для сохранения.")
                continue
            to_dump = []
            for v in vacancies:
                to_dump.append({"name": v.name, "url": v.url, "salary_range": v.salary_range, "snippet": v.snippet})
            file_handler.write_vacs(to_dump, indent=2)
            print("Вакансии сохранены в vacancies.json")

        # 5) Загрузить вакансии из файла и восстановить объекты Vacancy
        elif choice == "5":
            try:
                data = file_handler.load_vacs()
                vacancies = []
                for d in data:
                    vacancies.append(Vacancy(d["name"], d["url"], d.get("salary_range"), d.get("snippet", {})))
                print(f"Загружено {len(vacancies)} вакансий из файла.")
            except Exception as e:
                print("Ошибка при загрузке:", e)

        elif choice == "6":
            file_handler.clear()
            print("Сохранённые данные удаленны.")

        else:
            print("Неверный выбор, попробуйте ещё раз.")


user_interaction()
