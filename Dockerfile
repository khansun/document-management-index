FROM python:3.13-alpine

WORKDIR /app

RUN apk update && apk add linux-headers \
    python3-dev \
    libpq-dev \
    libc-dev \
    imagemagick \
    gcc \
    poppler-utils


COPY poetry.lock pyproject.toml README.md LICENSE /app/

RUN pip install --upgrade poetry

COPY i3worker /app/i3worker/
COPY logging.yaml /app/i3worker/logging.yaml

RUN poetry install -E pg -v

VOLUME ["/app/logs"]

CMD ["poetry", "run", "celery", "-A", "i3worker.celery_app", "worker", "-E", "--loglevel=DEBUG"]