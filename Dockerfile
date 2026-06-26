FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app/src

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml requirements.txt ./
COPY src ./src
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install -e .

COPY app ./app
COPY scripts ./scripts
COPY data ./data
COPY assets ./assets
COPY reports ./reports

RUN mkdir -p data/sample data/processed reports assets/demo assets/screenshots

EXPOSE 8501

CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
