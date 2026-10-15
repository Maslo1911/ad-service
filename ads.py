from collections.abc import Mapping
from datetime import date
from typing import Optional


class User:
    def __init__(self, name: str) -> None:
        name = name.strip()
        if not name:
            raise ValueError("Имя пользователя не должно быть пустым.")
        self.name = name

    def __str__(self) -> str:
        return self.name

    def has_name(self, name: str) -> bool:
        return self.name.casefold() == name.strip().casefold()


class Category:
    def __init__(self, name: str) -> None:
        name = name.strip()
        if not name:
            raise ValueError("Название категории не должно быть пустым.")
        self.name = name

    def __str__(self) -> str:
        return self.name

    def has_name(self, name: str) -> bool:
        return self.name.casefold() == name.strip().casefold()


class Ad:
    MAX_ACTIVE_DAYS = 30

    def __init__(
        self,
        ad_id: int,
        title: str,
        category: Category,
        price: int,
        seller: User,
        publish_date: date,
        is_active: bool = True,
    ) -> None:
        title = title.strip()
        if ad_id < 1:
            raise ValueError(
                "Идентификатор объявления должен быть положительным."
            )
        if not title:
            raise ValueError("Название объявления не должно быть пустым.")
        if price < 0:
            raise ValueError("Цена объявления не может быть отрицательной.")

        self.id = ad_id
        self.title = title
        self.category = category
        self.price = price
        self.seller = seller
        self.publish_date = publish_date
        self.is_active = is_active

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.title} | {self.category} | "
            f"{self.price} руб. | {self.seller} | {self.status}"
        )

    @property
    def status(self) -> str:
        return self.get_status()

    def get_status(self, max_active_days: int = MAX_ACTIVE_DAYS) -> str:
        if not self.is_active:
            return "Объявление снято с публикации"
        if self.is_expired(max_active_days):
            return "Срок размещения объявления истёк"
        return "Объявление активно и видно пользователям"

    def is_expired(self, max_active_days: int = MAX_ACTIVE_DAYS) -> bool:
        days_passed = (date.today() - self.publish_date).days
        return days_passed > max_active_days

    def deactivate(self) -> None:
        self.is_active = False

    def matches_title(self, query: str) -> bool:
        return query.casefold() in self.title.casefold()

    def belongs_to(self, category: str) -> bool:
        return self.category.has_name(category)

    def is_sold_by(self, seller_name: str) -> bool:
        return self.seller.has_name(seller_name)

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category.name,
            "price": self.price,
            "seller_name": self.seller.name,
            "publish_date": self.publish_date.isoformat(),
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "Ad":
        is_active = data.get("is_active", True)
        if not isinstance(is_active, bool):
            raise ValueError("Поле is_active должно иметь логический тип.")

        return cls(
            ad_id=int(data["id"]),
            title=str(data["title"]),
            category=Category(str(data["category"])),
            price=int(data["price"]),
            seller=User(str(data["seller_name"])),
            publish_date=date.fromisoformat(str(data["publish_date"])),
            is_active=is_active,
        )


def add_ad(
    ads: list[Ad],
    title: str,
    category: Category,
    price: int,
    seller: User,
) -> Ad:
    new_id = max((ad.id for ad in ads), default=0) + 1
    new_ad = Ad(
        ad_id=new_id,
        title=title,
        category=category,
        price=price,
        seller=seller,
        publish_date=date.today(),
    )
    ads.append(new_ad)
    return new_ad


def find_ads(ads: list[Ad], query: str) -> list[Ad]:
    return [ad for ad in ads if ad.matches_title(query)]


def filter_ads_by_category(ads: list[Ad], category: str) -> list[Ad]:
    return [ad for ad in ads if ad.belongs_to(category)]


def get_category_names(ads: list[Ad]) -> list[str]:
    names: dict[str, str] = {}
    for ad in ads:
        names.setdefault(ad.category.name.casefold(), ad.category.name)
    return sorted(names.values(), key=str.casefold)


def find_ads_by_seller(ads: list[Ad], seller_name: str) -> list[Ad]:
    return [ad for ad in ads if ad.is_sold_by(seller_name)]


def filter_ads_by_price(ads: list[Ad], max_price: int) -> list[Ad]:
    return [ad for ad in ads if ad.price <= max_price]


def sort_ads_by_price(
    ads: list[Ad],
    reverse: bool = False,
) -> list[Ad]:
    return sorted(ads, key=lambda ad: ad.price, reverse=reverse)


def find_ad_by_id(ads: list[Ad], ad_id: int) -> Optional[Ad]:
    for ad in ads:
        if ad.id == ad_id:
            return ad
    return None


def deactivate_ad(ads: list[Ad], ad_id: int) -> bool:
    ad = find_ad_by_id(ads, ad_id)
    if ad is None:
        return False
    ad.deactivate()
    return True


def get_stats(ads: list[Ad]) -> dict[str, int | float]:
    active_ads = [ad for ad in ads if ad.is_active]
    total = len(ads)
    active = len(active_ads)
    average_price = (
        sum(ad.price for ad in active_ads) / active if active_ads else 0
    )
    return {
        "total": total,
        "active": active,
        "average_price": round(average_price, 2),
    }
