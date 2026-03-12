from datetime import datetime
from uuid import UUID

from redis_practice.entities.typehints import ReportType
from redis_practice.providers.orders import OrdersRedisProvider
from redis_practice.providers.reports import ReportsRedisProvider
from redis_practice.redis_client import redis_client
from redis_practice.services.orders_mapper import OrdersMapper


def create_report_task(
    report_uuid: UUID,
    gte_date: datetime,
    lte_date: datetime,
) -> ReportType:
    """Задача для создания отчёта

    Args:
        report_uuid (UUID): uuid отчёта
        gte_date (datetime): дата от которой будут браться заказы для отчёта
        lte_date (datetime): дата до которой будут браться заказы для отчёта
    """
    orders = OrdersRedisProvider(redis_client).get_by_date_range(
        date_lte=lte_date, date_gte=gte_date
    )
    report = OrdersMapper().mapping(report_uuid=str(report_uuid), order_list=orders)

    ReportsRedisProvider(redis_client).send(report)

    return report
