FROM python:3.13-slim AS base

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y libmagic1

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN mkdir -p /app/uploads

EXPOSE 8000
EXPOSE 5678


FROM base AS dev

RUN pip install --no-cache-dir pytest debugpy

CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


FROM base AS test

COPY tests ./tests

RUN pip install --no-cache-dir pytest

CMD ["pytest"]


FROM base AS prod

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]