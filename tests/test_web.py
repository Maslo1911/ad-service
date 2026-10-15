"""Проверка страниц веб-интерфейса Django (ПР5)."""

import os
from datetime import date

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adservice.settings")
django.setup()

from django.test import Client, override_settings  # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402

from ads import Ad, Category, User  # noqa: E402
from storage import save_ads  # noqa: E402

setup_test_environment()


@pytest.fixture
def client(tmp_path):
    ads = [
        Ad(1, "Горный велосипед", Category("Транспорт"), 15000,
           User("Иван"), date.today()),
        Ad(2, "Диван <угловой>", Category("Мебель"), 8000,
           User("Мария"), date.today()),
        Ad(3, "Самокат", Category("Транспорт"), 2500,
           User("Иван"), date.today(), is_active=False),
    ]
    data_file = tmp_path / "ads.json"
    save_ads(str(data_file), ads)
    with override_settings(ADS_DATA_FILE=data_file):
        yield Client()


def test_index_page(client):
    response = client.get("/")
    text = response.content.decode()
    assert response.status_code == 200
    assert "Сервис объявлений" in text
    assert "bootstrap" in text


def test_ads_page_lists_all_ads(client):
    response = client.get("/ads/")
    text = response.content.decode()
    assert response.status_code == 200
    assert "Горный велосипед" in text
    assert "Самокат" in text
    assert "снято с публикации" in text


def test_ads_page_escapes_html(client):
    text = client.get("/ads/").content.decode()
    assert "Диван &lt;угловой&gt;" in text
    assert "<угловой>" not in text


def test_ads_page_sorted_by_price(client):
    text = client.get("/ads/?sort=price").content.decode()
    assert text.index("Самокат") < text.index("Диван")
    assert text.index("Диван") < text.index("Горный велосипед")


def test_ad_detail_page(client):
    response = client.get("/ads/1/")
    text = response.content.decode()
    assert response.status_code == 200
    assert "Горный велосипед" in text
    assert "15000 руб." in text
    assert "Иван" in text


def test_missing_ad_returns_404(client):
    response = client.get("/ads/999/")
    assert response.status_code == 404
    assert "Объявление не найдено" in response.content.decode()


def test_categories_page(client):
    response = client.get("/categories/")
    text = response.content.decode()
    assert response.status_code == 200
    assert "Мебель" in text
    assert "Транспорт" in text


def test_category_detail_page(client):
    response = client.get("/categories/Транспорт/")
    text = response.content.decode()
    assert response.status_code == 200
    assert "Горный велосипед" in text
    assert "Диван" not in text


def test_missing_category_returns_404(client):
    response = client.get("/categories/Нет такой/")
    assert response.status_code == 404


@override_settings(DEBUG=False)
def test_unknown_url_uses_custom_404_page(client):
    response = client.get("/nonexistent/")
    assert response.status_code == 404
    assert "404 – страница не найдена" in response.content.decode()
