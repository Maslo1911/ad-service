import json

def load_ads(filename: str) -> list[dict]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, начинаем с пустого списка.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, начинаем с пустого списка.")
        return []


def save_ads(filename: str, ads: list[dict]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(ads, file, ensure_ascii=False, indent=2)
