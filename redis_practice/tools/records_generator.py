from collections.abc import Generator
from datetime import datetime
from random import randint
from uuid import uuid4

from faker import Faker
from pytz import UTC

from redis_practice.entities.typehints import OrderItemType, OrderType

FOOD_NAMES = [
    "Пицца по баварски",
    "Кола",
    "Бургер",
    "Панцакота",
    "Фрикадельки",
    "Салат с курицей",
    "Омлет",
    "Хлеб",
    "Мясо",
    "Рыба",
    "Грибы",
    "Яйца",
    "Вареники",
    "Котлеты",
    "Тост",
    "Закуска",
    "Пирожное",
    "Суп",
    "Лапша",
    "Плов",
    "Пельмени",
    "Шашлык",
    "Пицца с крабом",
    "Сэндвич",
    "Кекс",
    "Мороженое",
    "Хачапури",
    "Закуски",
    "Панкейки",
    "Блинчики",
    "Филе тунца",
    "Котлеты из рыбы",
    "Курочка фри",
    "Гамбургер",
    "Салат с курицей и винегретом",
    "Мясной рулет",
    "Чизкейк",
    "Торт",
    "Пицца с колбасой",
    "Суп пельменный",
    "Квашеная капуста",
    "Фрукты",
    "Рыба в сливочном соусе",
    "Яичница фрил",
    "Картофель фри",
    "Пицца с печенью",
    "Гамбургер с курицей",
    "Салат с яблоком и сыром",
    "Котлеты из рыбы с картошкой",
    "Блинчики с боровиками",
    "Торт с шоколадной начинкой",
    "Пицца с мясом и грибами",
    "Закуска из овощей",
    "Салат с курицей и орегано",
    "Мясные пирожки",
    "Фруктовый салат",
    "Котлеты из свинины",
    "Панкейки с фруктами",
    "Гамбургер с беконом",
    "Суп с курицей",
    "Закуска из рыбы",
    "Блинчики с творогом",
    "Торт со сливочным кремом",
    "Пицца с колбасой и сыром",
    "Салат с винегретом и яйцом",
    "Рыба в горчичном соусе",
]


class OrdersGenerator:
    """Генератор заказов клиентов"""

    def __init__(self, fake: Faker) -> None:
        self._fake = fake

    def gen_item(self) -> OrderItemType:
        """Метод для генерации позиции заказа клиента

        Returns:
            OrderItemType: Позиция заказа клиента
        """

        return {
            "item_name": FOOD_NAMES[randint(0, len(FOOD_NAMES) - 1)],
            "price": randint(100, 10000) + round(randint(0, 100) / 100, 2),
            "discount": randint(1, 100) + round(randint(0, 100) / 100, 2),
            "count": randint(1, 10),
        }

    def gen_order(self, items_count: int = 1) -> OrderType:
        """Метод для генерации заказа клиента

        Args:
            items_count (int, optional): количество позиций в заказе клиента

        Returns:
            OrderType: Заказ клиента
        """
        items = []
        for _ in range(items_count):
            items.append(self.gen_item())

        return {
            "address_delivery": self._fake.address(),
            "created_at": str(
                self._fake.date_time_between(
                    datetime(2026, 1, 1, tzinfo=UTC),
                    datetime(2026, 1, 31, tzinfo=UTC),
                    tzinfo=UTC,
                )
            ),
            "full_name": self._fake.name(),
            "items": items,
            "number_phone": self._fake.phone_number(),
            "order_id": str(uuid4()),
            "price_delivery": randint(100, 200) + round(randint(0, 100) / 100, 2),
        }

    def gen_orders(
        self,
        count: int,
        max_items_per_order: int = 5,
    ) -> Generator[OrderType]:
        """Метод для генерации заказов клиентов

        Args:
            count (int): количество заказов
            max_items_per_order (int, optional): максимальное кол-во позиций в заказе

        Yields:
            Generator[OrderType]: Заказ клиента
        """
        for _ in range(count):
            yield self.gen_order(randint(1, max_items_per_order))
