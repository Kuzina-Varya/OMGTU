FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml .
RUN uv sync --no-cache

COPY consumer.py .

CMD ["uv", "run", "python", "consumer.py"]