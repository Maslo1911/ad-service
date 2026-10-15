import json

from ads import Ad


def load_ads(filename: str) -> list[Ad]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_ads = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, начинаем с пустого списка.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, начинаем с пустого списка.")
        return []

    if not isinstance(raw_ads, list):
        print(f"Файл {filename} имеет неверный формат, начинаем с пустого "
              "списка.")
        return []

    ads = []
    for raw_ad in raw_ads:
        try:
            ads.append(Ad.from_dict(raw_ad))
        except (KeyError, TypeError, ValueError, AttributeError) as error:
            print(f"Пропущено некорректное объявление {raw_ad!r}: {error}")
    return ads


def save_ads(filename: str, ads: list[Ad]) -> bool:
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [ad.to_dict() for ad in ads],
                file,
                ensure_ascii=False,
                indent=2,
            )
    except OSError as error:
        print(f"Не удалось сохранить данные в {filename}: {error}")
        return False
    return True
