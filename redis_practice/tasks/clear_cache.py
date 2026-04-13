from redis_practice.providers.orders import OrdersRedisProvider
from redis_practice.redis_client import redis_client


async def clear_cache_task() -> None:
    """Задача для чистки кеша (раз в сутки)"""
    provider = OrdersRedisProvider(redis_client)
    provider.clear()
