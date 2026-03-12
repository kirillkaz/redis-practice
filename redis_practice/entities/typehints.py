from enum import StrEnum
from typing import TypedDict


class QueuesEnum(StrEnum):
    """Enum с названиями очередей"""

    GEN_QUEUE = "gen_queue"
    API_QUEUE = "api_queue"


type DateStr = str


class OrderItemType(TypedDict):
    """Тип позиции заказа клиента"""

    item_name: str
    price: float
    discount: float
    count: int


class OrderType(TypedDict):
    """Тип заказа клиента"""

    order_id: str
    created_at: str
    items: list[OrderItemType]
    number_phone: str
    full_name: str
    address_delivery: str
    price_delivery: float


class RecordItemType(TypedDict):
    """Тип элемента отчёта. Информация по позиции за дату"""

    name_item: str
    total_count: int
    total_sum: float
    total_discount: float


class RecordDateItemType(TypedDict):
    """Тип элемента отчёта. Информация за дату"""

    total_sum: float
    total_count: int
    total_discount: float
    items: list[RecordItemType]


class ReportType(TypedDict):
    """Тип отчёта заказов клиентов"""

    report_uuid: str
    total_sum: float
    total_discount: float
    total_items: int
    dates: dict[DateStr, RecordDateItemType]
