from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.templatetags.static import static
from django.urls import reverse

from ads import Ad, get_category_names, get_stats
from storage import load_ads

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)

NAV_ITEMS = (
    ("index", "Главная"),
    ("ads", "Объявления"),
    ("categories", "Категории"),
)


def load_project_ads() -> list[Ad]:
    return load_ads(str(settings.ADS_DATA_FILE))


def page(title: str, content: str) -> str:
    links = "".join(
        f'<a class="nav-link" href="{reverse(name)}">{label}</a>'
        for name, label in NAV_ITEMS
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
    <link rel="stylesheet" href="{static('homepage/css/style.css')}">
</head>
<body>
    <nav class="navbar navbar-expand navbar-dark bg-primary mb-4">
        <div class="container">
            <a class="navbar-brand" href="{reverse('index')}">
                Сервис объявлений
            </a>
            <div class="navbar-nav">{links}</div>
        </div>
    </nav>
    <main class="container">{content}</main>
    <footer class="container site-footer">
        Сервис объявлений · учебный проект
    </footer>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    ads = load_project_ads()
    stats = get_stats(ads)
    categories_count = len(get_category_names(ads))
    content = f"""
    <h1 class="display-5">Сервис объявлений</h1>
    <p class="lead">
        Публикация, поиск и просмотр частных объявлений о продаже
        товаров и услуг.
    </p>
    <div class="row g-3 mb-4">
        <div class="col-sm-4">
            <div class="card stat-card"><div class="card-body">
                <div class="stat-value">{stats['total']}</div>
                <div class="text-muted">всего объявлений</div>
            </div></div>
        </div>
        <div class="col-sm-4">
            <div class="card stat-card"><div class="card-body">
                <div class="stat-value">{stats['active']}</div>
                <div class="text-muted">не сняты с публикации</div>
            </div></div>
        </div>
        <div class="col-sm-4">
            <div class="card stat-card"><div class="card-body">
                <div class="stat-value">{categories_count}</div>
                <div class="text-muted">категорий</div>
            </div></div>
        </div>
    </div>
    <p>Основные разделы:</p>
    <a href="{reverse('ads')}" class="btn btn-primary me-2">Объявления</a>
    <a href="{reverse('categories')}" class="btn btn-secondary">
        Категории
    </a>
    """
    return HttpResponse(page("Сервис объявлений", content))


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    content = f"""
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="{reverse('index')}" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
