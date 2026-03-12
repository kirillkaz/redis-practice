from redis_practice.redis_client import redis_client
from redis_practice.providers.orders import OrdersRedisProvider
from redis_practice.providers.reports import ReportsRedisProvider


async def orders_provider_depend() -> OrdersRedisProvider:
    """Зависимость для создания провайдера заказов"""
    return OrdersRedisProvider(redis_client)


async def reports_provider_depend() -> ReportsRedisProvider:
    """Зависимость для создания провайдера отчётов"""
    return ReportsRedisProvider(redis_client)
