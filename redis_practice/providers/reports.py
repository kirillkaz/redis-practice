import json
from uuid import UUID

from redis.asyncio import Redis

from redis_practice.entities.typehints import ReportType


class ReportsRedisProvider:
    """Провайдер Redis для отчётов заказов клиентов"""

    KEY_PREFIX = "reports"
    KEY_TTL = 600

    def __init__(self, conn: Redis) -> None:
        self._conn = conn

    @property
    def data_key(self) -> str:
        return self.KEY_PREFIX + ":" + "data"

    def send(self, report: ReportType) -> None:
        """Метод для отправки отчёта в Redis"""
        if report:
            pipe = self._conn.pipeline()
            pipe.hset(
                self.data_key,
                report["report_uuid"],
                value=json.dumps(report, ensure_ascii=False),
            )
            pipe.expire(self.data_key, self.KEY_TTL)
            pipe.execute()

    def get(self, report_uuid: UUID) -> ReportType:
        """Метод для получения отчёта по его uuid

        Args:
            report_uuid (UUID): uuid отчёта

        Returns:
            ReportType: Отчёт заказов клиентов
        """
        report_raw = self._conn.hget(self.data_key, str(report_uuid))
        return json.loads(report_raw)
