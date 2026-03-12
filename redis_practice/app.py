from faker import Faker
from fastapi import FastAPI

from redis_practice.api.endpoints.reports import reports_router

fake = Faker()
app = FastAPI()

app.include_router(reports_router)
