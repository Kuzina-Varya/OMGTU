FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml .
RUN uv sync --no-cache

COPY dashboard.py .

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "dashboard.py", "--server.address=0.0.0.0", "--server.port=8501"]