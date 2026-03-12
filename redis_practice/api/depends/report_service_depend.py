from typing import Annotated

from fastapi import Depends

from redis_practice.providers.orders import OrdersRedisProvider
from redis_practice.providers.reports import ReportsRedisProvider
from redis_practice.services.orders_mapper import OrdersMapper
from redis_practice.services.reports import ReportCreateService

from .mappers_depends import orders_mapper_depend
from .providers_depends import orders_provider_depend, reports_provider_depend


async def report_service_depend(
    orders_mapper: Annotated[OrdersMapper, Depends(orders_mapper_depend)],
    orders_provider: Annotated[OrdersRedisProvider, Depends(orders_provider_depend)],
    reports_provider: Annotated[ReportsRedisProvider, Depends(reports_provider_depend)],
) -> ReportCreateService:
    """Зависимость для создания сервиса для работы с отчётами

    Args:
        orders_mapper (Annotated[OrdersMapper, Depends): маппер заказов
        orders_provider (Annotated[OrdersRedisProvider, Depends): провайдер заказов
        reports_provider (Annotated[ReportsRedisProvider, Depends): провайдер отчётов

    Returns:
        ReportCreateService: Сервис для работы с отчётами
    """
    return ReportCreateService(
        orders_mapper=orders_mapper,
        reports_provider=reports_provider,
        orders_provider=orders_provider,
    )
