from datetime import date

ad_title = "Продам горный велосипед"
category = "Транспорт"
price = 15500
seller_name = "Иван Петров"
publish_date = date(2026, 9, 1)
is_active = True
max_active_days = 30

# --- Операции и преобразование типов ---
price_with_discount = price - 500
price_str = str(price_with_discount)
today = date.today()
days_since_publish = (today - publish_date).days


# --- Ветвления ---
def get_ad_status(active: bool, days_passed: int, max_days: int) -> str:
    if not active:
        return "Объявление снято с публикации"
    elif days_passed > max_days:
        return "Срок размещения объявления истёк"
    else:
        return "Объявление активно и видно пользователям"


print(f"Объявление: {ad_title}")
print(f"Категория: {category}")
print(f"Автор: {seller_name}")
print(f"Цена со скидкой: {price_str} руб.")
print(f"Дата публикации: {publish_date}")
print(f"Дней с момента публикации: {days_since_publish}")
print(get_ad_status(is_active, days_since_publish, max_active_days))