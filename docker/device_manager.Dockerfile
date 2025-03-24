FROM python:3.12-slim-bookworm

WORKDIR /app

COPY pyproject.toml /app
COPY poetry.lock /app

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY /device_manager /app/device_manager
COPY /models /app/models
COPY /orchestration /app/orchestration
COPY /drivers /app/drivers

CMD [ "poetry", "run", "python", "-m","device_manager" ]