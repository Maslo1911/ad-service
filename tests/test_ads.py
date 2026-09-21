"""Автоматизированные тесты функций модуля ads."""

from ads import (
    add_ad,
    deactivate_ad,
    filter_ads_by_category,
    find_ads,
    get_ad_status,
    sort_ads_by_price,
)


def test_add_ad():
    ads = []
    add_ad(ads, "Продам велосипед", "Транспорт", 15000, "Иван")
    assert len(ads) == 1
    assert ads[0]["is_active"] is True


def test_find_ads():
    ads = []
    add_ad(ads, "Продам велосипед", "Транспорт", 15000, "Иван")
    assert find_ads(ads, "велосипед")
    assert not find_ads(ads, "автомобиль")


def test_filter_ads_by_category():
    ads = []
    add_ad(ads, "Продам велосипед", "Транспорт", 15000, "Иван")
    add_ad(ads, "Продам диван", "Мебель", 8000, "Пётр")
    result = filter_ads_by_category(ads, "Мебель")
    assert len(result) == 1
    assert result[0]["title"] == "Продам диван"


def test_sort_ads_by_price():
    ads = []
    add_ad(ads, "Дорогой товар", "Разное", 5000, "Иван")
    add_ad(ads, "Дешёвый товар", "Разное", 1000, "Пётр")
    sorted_ads = sort_ads_by_price(ads)
    assert sorted_ads[0]["price"] == 1000


def test_deactivate_ad():
    ads = []
    ad = add_ad(ads, "Продам велосипед", "Транспорт", 15000, "Иван")
    assert deactivate_ad(ads, ad["id"]) is True
    assert get_ad_status(ad) == "Объявление снято с публикации"


def test_deactivate_missing_ad_returns_false():
    ads = []
    assert deactivate_ad(ads, 999) is False
