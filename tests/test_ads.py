"""Автоматизированные тесты объектной модели и функций модуля ads."""

from datetime import date, timedelta

import pytest

from ads import (
    Ad,
    Category,
    User,
    add_ad,
    deactivate_ad,
    filter_ads_by_category,
    find_ads,
    find_ads_by_seller,
    get_category_names,
    get_stats,
    sort_ads_by_price,
)
from storage import load_ads, save_ads


def make_ad(ads: list[Ad], title: str, category: str, price: int,
            seller: str) -> Ad:
    return add_ad(ads, title, Category(category), price, User(seller))


def test_add_ad_creates_active_object():
    ads = []
    ad = make_ad(ads, "Продам велосипед", "Транспорт", 15000, "Иван")
    assert ads == [ad]
    assert isinstance(ad, Ad)
    assert ad.id == 1
    assert ad.is_active is True


def test_add_ad_generates_next_id():
    ads = []
    make_ad(ads, "Велосипед", "Транспорт", 15000, "Иван")
    second = make_ad(ads, "Диван", "Мебель", 8000, "Пётр")
    assert second.id == 2


def test_ad_rejects_negative_price():
    with pytest.raises(ValueError):
        make_ad([], "Велосипед", "Транспорт", -1, "Иван")


def test_user_rejects_empty_name():
    with pytest.raises(ValueError):
        User("   ")


def test_ad_str_contains_main_fields():
    ad = make_ad([], "Продам велосипед", "Транспорт", 15000, "Иван")
    text = str(ad)
    assert "Продам велосипед" in text
    assert "Транспорт" in text
    assert "15000 руб." in text
    assert "Иван" in text


def test_find_ads():
    ads = []
    make_ad(ads, "Продам велосипед", "Транспорт", 15000, "Иван")
    assert find_ads(ads, "ВЕЛОСИПЕД")
    assert not find_ads(ads, "автомобиль")


def test_filter_ads_by_category():
    ads = []
    make_ad(ads, "Продам велосипед", "Транспорт", 15000, "Иван")
    make_ad(ads, "Продам диван", "Мебель", 8000, "Пётр")
    result = filter_ads_by_category(ads, "мебель")
    assert [ad.title for ad in result] == ["Продам диван"]


def test_find_ads_by_seller():
    ads = []
    make_ad(ads, "Велосипед", "Транспорт", 15000, "Иван")
    make_ad(ads, "Диван", "Мебель", 8000, "Пётр")
    make_ad(ads, "Самокат", "Транспорт", 3000, "Иван")
    result = find_ads_by_seller(ads, "иван")
    assert [ad.title for ad in result] == ["Велосипед", "Самокат"]


def test_sort_ads_by_price():
    ads = []
    make_ad(ads, "Дорогой товар", "Разное", 5000, "Иван")
    make_ad(ads, "Дешёвый товар", "Разное", 1000, "Пётр")
    assert [ad.price for ad in sort_ads_by_price(ads)] == [1000, 5000]


def test_deactivate_ad():
    ads = []
    ad = make_ad(ads, "Продам велосипед", "Транспорт", 15000, "Иван")
    assert deactivate_ad(ads, ad.id) is True
    assert ad.status == "Объявление снято с публикации"


def test_deactivate_missing_ad_returns_false():
    assert deactivate_ad([], 999) is False


def test_expired_ad_status():
    ad = Ad(
        ad_id=1,
        title="Старое объявление",
        category=Category("Разное"),
        price=100,
        seller=User("Иван"),
        publish_date=date.today() - timedelta(days=Ad.MAX_ACTIVE_DAYS + 1),
    )
    assert ad.status == "Срок размещения объявления истёк"


def test_is_expired():
    ad = make_ad([], "Велосипед", "Транспорт", 15000, "Иван")
    assert ad.is_expired() is False
    ad.publish_date = date.today() - timedelta(days=Ad.MAX_ACTIVE_DAYS + 1)
    assert ad.is_expired() is True


def test_get_category_names_unique_and_sorted():
    ads = []
    make_ad(ads, "Велосипед", "Транспорт", 15000, "Иван")
    make_ad(ads, "Диван", "Мебель", 8000, "Пётр")
    make_ad(ads, "Самокат", "транспорт", 3000, "Иван")
    assert get_category_names(ads) == ["Мебель", "Транспорт"]


def test_get_stats_counts_only_active_for_average():
    ads = []
    make_ad(ads, "Велосипед", "Транспорт", 1000, "Иван")
    sold = make_ad(ads, "Диван", "Мебель", 9000, "Пётр")
    sold.deactivate()
    assert get_stats(ads) == {"total": 2, "active": 1, "average_price": 1000}


def test_to_dict_and_from_dict_roundtrip():
    ad = make_ad([], "Продам велосипед", "Транспорт", 15000, "Иван")
    restored = Ad.from_dict(ad.to_dict())
    assert restored.to_dict() == ad.to_dict()
    assert isinstance(restored.seller, User)
    assert isinstance(restored.category, Category)


def test_save_and_load_ads(tmp_path):
    filename = tmp_path / "ads.json"
    ads = []
    make_ad(ads, "Продам велосипед", "Транспорт", 15000, "Иван")
    assert save_ads(str(filename), ads) is True

    loaded = load_ads(str(filename))
    assert len(loaded) == 1
    assert loaded[0].title == "Продам велосипед"
    assert loaded[0].seller.name == "Иван"


def test_load_missing_file_returns_empty_list(tmp_path):
    assert load_ads(str(tmp_path / "missing.json")) == []


def test_load_corrupted_file_returns_empty_list(tmp_path):
    filename = tmp_path / "ads.json"
    filename.write_text("{не json", encoding="utf-8")
    assert load_ads(str(filename)) == []


def test_load_skips_invalid_records(tmp_path):
    filename = tmp_path / "ads.json"
    filename.write_text(
        '[{"id": 1, "title": "Без цены"}, '
        '{"id": 2, "title": "Диван", "category": "Мебель", "price": 8000, '
        '"seller_name": "Пётр", "publish_date": "2026-09-10", '
        '"is_active": true}]',
        encoding="utf-8",
    )
    loaded = load_ads(str(filename))
    assert [ad.id for ad in loaded] == [2]
