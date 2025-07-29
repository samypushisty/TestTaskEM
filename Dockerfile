FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH="${PYTHONPATH}:/app/application"

COPY pyproject.toml poetry.lock ./
COPY application/ ./application/

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

CMD ["sh", "-c", "alembic -c application/alembic.ini upgrade head && python application/add_values.py && uvicorn application.main:main_app --host 0.0.0.0 --port 8000"]