from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from redis_practice.entities.typehints import DateStr


class GetReportsQuerySchema(BaseModel):
    """Модель для запроса на получение данных отчёта"""

    report_uuid: UUID


class CreateReportsBodySchema(BaseModel):
    """Модель для запроса на создание данных отчёта"""

    lte_date: datetime
    gte_date: datetime


class RecordItemSchema(BaseModel):
    """Валидационная модель элемента отчёта. Информация по позиции за дату"""

    name_item: str
    total_count: int
    total_sum: float
    total_discount: float


class RecordDateItemSchema(BaseModel):
    """Валидационная модель элемента отчёта. Информация за дату"""

    total_sum: float
    total_count: int
    total_discount: float
    items: list[RecordItemSchema]


class ReportSchema(BaseModel):
    """Валидационная модель отчёта заказов клиентов"""

    report_uuid: str
    total_sum: float
    total_discount: float
    total_items: int
    dates: dict[DateStr, RecordDateItemSchema]
