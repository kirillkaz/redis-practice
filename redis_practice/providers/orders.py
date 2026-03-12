import json
from datetime import datetime
from logging import Logger
from typing import cast
from uuid import UUID

from dateutil.parser import parse
from redis.asyncio import Redis

from redis_practice.entities.typehints import DateStr, OrderType

logger = Logger(__name__)


class OrdersRedisProvider:
    """Провайдер Redis для заказов клиентов"""

    KEY_PREFIX = "orders"
    KEY_TTL = 180

    def __init__(self, conn: Redis) -> None:
        self._conn = conn

    @property
    def data_key(self) -> str:
        return self.KEY_PREFIX + ":" + "orders"

    @property
    def ordered_keys_key(self) -> str:
        return self.KEY_PREFIX + ":" + "orders_sorted_keys"

    def send(self, order: OrderType) -> None:
        """Метод для отправки заказа пользователя в Redis"""
        order_value = int(parse(order["created_at"]).timestamp())
        logger.info(order)
        pipe = self._conn.pipeline()
        pipe.zadd(
            self.ordered_keys_key, {order["order_id"]: order_value}
        )  # TODO: будет бесконечно расти. :(
        pipe.hsetex(
            self.data_key,
            order["order_id"],
            value=json.dumps(order),
            ex=self.KEY_TTL,
        )

        pipe.execute()

    def get_by_id(
        self,
        order_id: UUID,
    ) -> OrderType:
        """Метод для получения заказа клиента по id"""
        result = self._conn.hget(self.data_key, str(order_id))
        return json.loads(result)

    def get_by_date_range(
        self,
        date_lte: DateStr,
        date_gte: DateStr,
    ) -> list[OrderType]:
        """Метод для получения списка заказов клиентов по временному отрезку

        Args:
            date_lte (datetime): Дата конца выборки
            date_gte (datetime): Дата начала выборки

        Returns:
            list[OrderType]: Список заказов клиентов
        """
        date_lte_int = int(parse(date_lte).timestamp())
        date_gte_int = int(parse(date_gte).timestamp())
        print(f"{self.ordered_keys_key=}")
        print(f"{date_lte_int=}")
        print(f"{date_gte_int=}")
        record_ids_raw = cast(
            list[bytes],
            self._conn.zrange(
                self.ordered_keys_key,
                date_gte_int,
                date_lte_int,
                byscore=True,
            ),
        )
        record_ids = [item.decode() for item in record_ids_raw]
        print(f"{record_ids=}")
        if record_ids:
            raw_result = self._conn.hmget(self.data_key, record_ids)
            result = [json.loads(record) for record in raw_result]
            return result
        return []
