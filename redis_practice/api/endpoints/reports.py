from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Body, HTTPException, Query
from rq.exceptions import NoSuchJobError
from rq.job import Job

from redis_practice.api.schemas.reports import (
    CreateReportsBodySchema,
    GetReportsQuerySchema,
    ReportSchema,
)
from redis_practice.queues import api_q
from redis_practice.redis_client import redis_client
from redis_practice.tasks.report import create_report_task

reports_router = APIRouter(prefix="/reports")


@reports_router.post(path="", summary="Создать отчёт заказов")
async def create_report(
    body: Annotated[CreateReportsBodySchema, Body(...)],
) -> UUID:
    """Route для создания отчёта заказов клиентов"""
    new_report_uuid = str(uuid4())

    job = api_q.enqueue(
        create_report_task,
        report_uuid=new_report_uuid,
        gte_date=str(body.gte_date),
        lte_date=str(body.lte_date),
        job_id=new_report_uuid,
    )
    return job.id


@reports_router.get(path="", summary="Получить отчёт заказов")
async def get_results_report(
    query: Annotated[GetReportsQuerySchema, Query(...)],
) -> ReportSchema:
    """Route для получения отчёта заказов клиентов"""
    try:
        job = Job.fetch(id=str(query.report_uuid), connection=redis_client)
    except NoSuchJobError as ex:
        raise HTTPException(
            status_code=422, detail=f"unknown task id: {query.report_uuid}"
        ) from ex
    result = job.result
    return result
