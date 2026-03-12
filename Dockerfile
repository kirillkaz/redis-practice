FROM python:3.12-slim

WORKDIR /usr/src

COPY . /usr/src
RUN pip install uv && uv sync

# Команда запуска зависит от сервиса в docker-compose
CMD ["uvicorn", "redis_practice.app:app", "--host", "0.0.0.0", "--port", "8000"]