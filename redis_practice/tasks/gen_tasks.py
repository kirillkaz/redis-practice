from random import randint

from redis_practice.app import fake
from redis_practice.providers.orders import OrdersRedisProvider
from redis_practice.redis_client import redis_client
from redis_practice.tools.records_generator import OrdersGenerator


async def gen_orders_task() -> None:
    """Задача для генерации заказов пользователей"""
    provider = OrdersRedisProvider(redis_client)
    generator = OrdersGenerator(fake)
    for order in generator.gen_orders(count=randint(4, 10)):
        # NOTE: отправляю не пачкой, так как имитирую заказы от разных пользователей
        provider.send(order)
