from redis_practice.services.orders_mapper import OrdersMapper


async def orders_mapper_depend() -> OrdersMapper:
    return OrdersMapper()
