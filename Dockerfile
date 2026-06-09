FROM python:3.13-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN mkdir -p /app/uploads

EXPOSE 8000


FROM base AS dev

RUN pip install --no-cache-dir pytest

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


FROM base AS test

COPY tests ./tests
RUN pip install --no-cache-dir pytest

CMD ["pytest"]


FROM base AS prod

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]