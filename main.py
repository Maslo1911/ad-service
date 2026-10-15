from ads import (
    Ad,
    Category,
    User,
    add_ad,
    deactivate_ad,
    filter_ads_by_category,
    find_ads,
    find_ads_by_seller,
    get_stats,
    sort_ads_by_price,
)
from storage import load_ads, save_ads
from utils import input_int, input_nonempty

DATA_FILE = "data/ads.json"

MENU = (
    "\n ===== Сервис объявлений ===== \n"
    "1. Показать все объявления\n"
    "2. Найти объявление по названию\n"
    "3. Показать объявления по категории\n"
    "4. Показать объявления по возрастанию цены\n"
    "5. Показать объявления продавца\n"
    "6. Добавить объявление\n"
    "7. Снять объявление с публикации\n"
    "8. Показать статистику\n"
    "0. Выход"
)


def show_ads(ads: list[Ad]) -> None:
    if not ads:
        print("Объявлений пока нет.")
        return
    for ad in ads:
        print(ad)


def show_stats(ads: list[Ad]) -> None:
    stats = get_stats(ads)
    print(
        f"Всего объявлений: {stats['total']}, "
        f"активных: {stats['active']}, "
        f"средняя цена активных: {stats['average_price']} руб."
    )


def handle_add_ad(ads: list[Ad]) -> None:
    title = input_nonempty("Название объявления: ")
    category = Category(input_nonempty("Категория: "))
    price = input_int("Цена: ")
    seller = User(input_nonempty("Ваше имя: "))
    try:
        new_ad = add_ad(ads, title, category, price, seller)
    except ValueError as error:
        print(f"Ошибка: {error}")
        return
    if save_ads(DATA_FILE, ads):
        print(f"Объявление добавлено: {new_ad}")


def handle_deactivate_ad(ads: list[Ad]) -> None:
    ad_id = input_int("Идентификатор объявления: ")
    if not deactivate_ad(ads, ad_id):
        print("Объявление с таким идентификатором не найдено.")
        return
    if save_ads(DATA_FILE, ads):
        print("Объявление снято с публикации.")


def main() -> None:
    ads = load_ads(DATA_FILE)

    actions = {
        "1": lambda: show_ads(ads),
        "2": lambda: show_ads(find_ads(ads, input_nonempty("Название: "))),
        "3": lambda: show_ads(
            filter_ads_by_category(ads, input_nonempty("Категория: "))
        ),
        "4": lambda: show_ads(sort_ads_by_price(ads)),
        "5": lambda: show_ads(
            find_ads_by_seller(ads, input_nonempty("Имя продавца: "))
        ),
        "6": lambda: handle_add_ad(ads),
        "7": lambda: handle_deactivate_ad(ads),
        "8": lambda: show_stats(ads),
    }

    while True:
        print(MENU)
        choice = input("Выберите действие: ")

        if choice == "0":
            print("До свидания!")
            break

        action = actions.get(choice)
        if action is None:
            print("Неизвестная команда, попробуйте снова.")
        else:
            print()
            action()


if __name__ == "__main__":
    main()
