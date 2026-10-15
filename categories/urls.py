from django.urls import path

from . import views

urlpatterns = [
    path("", views.categories, name="categories"),
    path(
        "<str:category_name>/",
        views.category_detail,
        name="category_detail",
    ),
]
