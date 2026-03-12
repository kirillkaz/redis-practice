from datetime import datetime
from uuid import UUID

from redis_practice.entities.typehints import ReportType
from redis_practice.providers.orders import OrdersRedisProvider
from redis_practice.providers.reports import ReportsRedisProvider
from redis_practice.services.orders_mapper import OrdersMapper


class ReportCreateService:
    def __init__(
        self,
        orders_provider: OrdersRedisProvider,
        reports_provider: ReportsRedisProvider,
        orders_mapper: OrdersMapper,
    ) -> None:
        self._reports_provider = reports_provider
        self._orders_provider = orders_provider
        self._orders_mapper = orders_mapper

    def create_report(
        self,
        report_uuid: UUID,
        gte_date: datetime,
        lte_date: datetime,
    ) -> None:
        """Метод для создания отчёта

        Args:
            report_uuid (UUID): uuid отчёта
            gte_date (datetime): дата от которой будут браться заказы для отчёта
            lte_date (datetime): дата до которой будут браться заказы для отчёта
        """
        orders = self._orders_provider.get_by_date_range(
            date_lte=lte_date, date_gte=gte_date
        )
        report = self._orders_mapper.mapping(
            report_uuid=str(report_uuid), order_list=orders
        )

        self._reports_provider.send(report)

        return report

    def get_report(self, report_uuid: UUID) -> ReportType:
        """Метод для получения отчёта

        Args:
            report_uuid (UUID): uuid отчёта

        Returns:
            ReportType: отчёт
        """
        # TODO: обработать отсутствие отчёта
        return self._reports_provider.get(report_uuid)
