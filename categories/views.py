from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.html import escape

from ads import filter_ads_by_category, get_category_names
from homepage.views import load_project_ads, page
from listings.views import render_ad_list


def categories(request: HttpRequest) -> HttpResponse:
    ads_list = load_project_ads()
    items = ""
    for name in get_category_names(ads_list):
        count = len(filter_ads_by_category(ads_list, name))
        url = reverse("category_detail", args=[name])
        items += f"""
        <li class="list-group-item d-flex justify-content-between
                   align-items-center">
            <a href="{url}">{escape(name)}</a>
            <span class="badge bg-primary rounded-pill">{count}</span>
        </li>
        """
    if not items:
        items = '<li class="list-group-item">Категорий пока нет.</li>'

    content = f"""
    <h1>Категории</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Категории", content))


def category_detail(request: HttpRequest, category_name: str) -> HttpResponse:
    ads_list = filter_ads_by_category(load_project_ads(), category_name)
    back_link = f"""
    <a href="{reverse('categories')}" class="btn btn-outline-secondary mt-3">
        ← к списку категорий
    </a>
    """
    if not ads_list:
        content = f"""
        <h1 class="text-danger">Категория не найдена</h1>
        {back_link}
        """
        return HttpResponse(
            page("Категория не найдена", content),
            status=404,
        )

    title = escape(ads_list[0].category.name)
    content = f"""
    <h1>Категория: {title}</h1>
    {render_ad_list(ads_list)}
    {back_link}
    """
    return HttpResponse(page(title, content))
