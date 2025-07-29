FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH="${PYTHONPATH}:/app/src"

COPY pyproject.toml poetry.lock ./
COPY src/ ./src/

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

CMD ["sh", "-c", "alembic -c src/alembic.ini upgrade head && python src/add_values.py && uvicorn src.main:main_app --host 0.0.0.0 --port 8000"]