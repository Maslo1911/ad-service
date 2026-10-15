"""Корневая маршрутизация проекта «Сервис объявлений»."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("ads/", include("listings.urls")),
    path("categories/", include("categories.urls")),
]

handler404 = "homepage.views.page_not_found"
