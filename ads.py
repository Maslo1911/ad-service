from datetime import date
from typing import Optional


def add_ad(
    ads: list[dict],
    title: str,
    category: str,
    price: int,
    seller_name: str,
) -> dict:

    new_id = max((ad["id"] for ad in ads), default=0) + 1
    new_ad = {
        "id": new_id,
        "title": title,
        "category": category,
        "price": price,
        "seller_name": seller_name,
        "publish_date": date.today().isoformat(),
        "is_active": True,
    }
    ads.append(new_ad)
    return new_ad


def find_ads(ads: list[dict], query: str) -> list[dict]:
    query_lower = query.lower()
    return [ad for ad in ads if query_lower in ad["title"].lower()]


def filter_ads_by_category(ads: list[dict], category: str) -> list[dict]:
    return [ad for ad in ads if ad["category"].lower() == category.lower()]


def filter_ads_by_price(ads: list[dict], max_price: int) -> list[dict]:
    return list(ad for ad in ads if ad["price"] <= max_price)


def sort_ads_by_price(ads: list[dict], reverse: bool = False) -> list[dict]:
    return sorted(ads, key=lambda ad: ad["price"], reverse=reverse)


def find_ad_by_id(ads: list[dict], ad_id: int) -> Optional[dict]:
    for ad in ads:
        if ad["id"] == ad_id:
            return ad
    return None


def deactivate_ad(ads: list[dict], ad_id: int) -> bool:
    ad = find_ad_by_id(ads, ad_id)
    if ad is None:
        return False
    ad["is_active"] = False
    return True


def get_ad_status(ad: dict, max_active_days: int = 30) -> str:
    if not ad["is_active"]:
        return "Объявление снято с публикации"

    publish_date = date.fromisoformat(ad["publish_date"])
    days_passed = (date.today() - publish_date).days
    if days_passed > max_active_days:
        return "Срок размещения объявления истёк"
    return "Объявление активно и видно пользователям"


def get_stats(ads: list[dict]) -> dict:
    active_ads = [ad for ad in ads if ad["is_active"]]
    total = len(ads)
    active = len(active_ads)
    if active_ads:
        avg_price = sum(ad["price"] for ad in active_ads) / active
    else:
        avg_price = 0
    return {
        "total": total,
        "active": active,
        "average_price": round(avg_price, 2),
    }
