import json
from datetime import datetime
from typing import cast
from uuid import UUID

import pytest
from rq import SimpleWorker
from rq.job import Job

from redis_practice.entities.typehints import OrderType, ReportType
from redis_practice.providers.orders import OrdersRedisProvider
from redis_practice.queues import api_q
from redis_practice.redis_client import redis_client
from redis_practice.tasks.report import create_report_task
from pathlib import Path

@pytest.fixture
def orders_test_data() -> list[OrderType]:
    """Фикстура для получения тестовых данных"""
    with open(Path.cwd() / "tests/orders_data.json") as f:
        data = cast(list[OrderType], json.load(f))
    return data


@pytest.fixture
def orders_provider() -> OrdersRedisProvider:
    """Фикстура для получения провайдера заказов"""
    return OrdersRedisProvider(redis_client)


@pytest.fixture
def preload_test_data(
    orders_test_data: list[OrderType], orders_provider: OrdersRedisProvider
) -> None:
    """Фикстура для помещения тестовых данных в redis"""
    for order in orders_test_data:
        orders_provider.send(order)


@pytest.mark.parametrize(
    ("report_uuid", "gte_date", "lte_date", "expected_data_path"),
    [
        (
            UUID("83ba1577-7d43-420c-a865-b43bfe569922"),
            datetime(2026, 1, 1),
            datetime(2026, 1, 31),
            Path.cwd() / "tests/report.json"
        )
    ],
)
def test_create_report_task(
    report_uuid: UUID,
    gte_date: datetime,
    lte_date: datetime,
    expected_data_path: Path,
    preload_test_data: None,
) -> None:
    with open(expected_data_path) as f:
        expected_data = cast(ReportType, json.load(f))

    api_q.enqueue(
        create_report_task,
        report_uuid=str(report_uuid),
        gte_date=str(gte_date),
        lte_date=str(lte_date),
        job_id=str(report_uuid),
    )
    worker = SimpleWorker([api_q], connection=api_q.connection)
    worker.work(burst=True)

    job = Job.fetch(id=str(report_uuid), connection=redis_client)
    job.result

    assert job.result == expected_data
