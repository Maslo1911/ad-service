from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.html import escape

from ads import Ad, find_ad_by_id, sort_ads_by_price
from homepage.views import load_project_ads, page

SORT_OPTIONS = (
    ("", "По умолчанию"),
    ("price", "Сначала дешевле"),
    ("-price", "Сначала дороже"),
)


def status_badge(ad: Ad) -> str:
    if not ad.is_active:
        css_class = "bg-secondary"
    elif ad.is_expired():
        css_class = "bg-warning text-dark"
    else:
        css_class = "bg-success"
    return f'<span class="badge {css_class}">{escape(ad.status)}</span>'


def render_ad_list(ads: list[Ad]) -> str:
    if not ads:
        return '<p class="text-muted">Объявлений пока нет.</p>'

    items = ""
    for ad in ads:
        url = reverse("ad_detail", args=[ad.id])
        items += f"""
        <li class="list-group-item d-flex justify-content-between
                   align-items-center">
            <div>
                <a href="{url}">{escape(ad.title)}</a>
                <div class="small text-muted">
                    {escape(ad.category.name)} · {escape(ad.seller.name)}
                </div>
            </div>
            <div class="text-end">
                <div class="fw-semibold">{ad.price} руб.</div>
                {status_badge(ad)}
            </div>
        </li>
        """
    return f'<ul class="list-group">{items}</ul>'


def render_sort_links(current: str) -> str:
    links = ""
    for value, label in SORT_OPTIONS:
        url = reverse("ads") + (f"?sort={value}" if value else "")
        style = "btn-primary" if value == current else "btn-outline-primary"
        links += f'<a href="{url}" class="btn btn-sm {style}">{label}</a>'
    return f'<div class="btn-group mb-3">{links}</div>'


def ads(request: HttpRequest) -> HttpResponse:
    ads_list = load_project_ads()
    sort = request.GET.get("sort", "")
    if sort == "price":
        ads_list = sort_ads_by_price(ads_list)
    elif sort == "-price":
        ads_list = sort_ads_by_price(ads_list, reverse=True)
    else:
        sort = ""

    content = f"""
    <h1>Объявления</h1>
    {render_sort_links(sort)}
    {render_ad_list(ads_list)}
    """
    return HttpResponse(page("Объявления", content))


def ad_detail(request: HttpRequest, ad_id: int) -> HttpResponse:
    ad = find_ad_by_id(load_project_ads(), ad_id)
    if ad is None:
        content = f"""
        <h1 class="text-danger">Объявление не найдено</h1>
        <a href="{reverse('ads')}" class="btn btn-outline-secondary">
            ← к списку объявлений
        </a>
        """
        return HttpResponse(
            page("Объявление не найдено", content),
            status=404,
        )

    category_url = reverse("category_detail", args=[ad.category.name])
    content = f"""
    <div class="card ad-card">
        <div class="card-body">
            <h5 class="card-title">{escape(ad.title)}</h5>
            <p class="card-text"><strong>ID:</strong> {ad.id}</p>
            <p class="card-text">
                <strong>Категория:</strong>
                <a href="{category_url}">{escape(ad.category.name)}</a>
            </p>
            <p class="card-text"><strong>Цена:</strong> {ad.price} руб.</p>
            <p class="card-text">
                <strong>Продавец:</strong> {escape(ad.seller.name)}
            </p>
            <p class="card-text">
                <strong>Дата публикации:</strong>
                {ad.publish_date.strftime('%d.%m.%Y')}
            </p>
            <p class="card-text">
                <strong>Статус:</strong> {status_badge(ad)}
            </p>
            <a href="{reverse('ads')}" class="btn btn-outline-secondary">
                ← к списку объявлений
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(escape(ad.title), content))
