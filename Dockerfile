FROM python:3.13.3-alpine3.21

COPY ./requirements/requirements.txt /tmp/requirements.txt
COPY ./requirements/requirements.dev.txt /tmp/requirements.dev.txt
COPY ./docker/local/django/celery_scripts /celery_scripts
COPY ./backend /backend

WORKDIR /backend

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install -U pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /backend/logs && \
    chown -R django-user:django-user /backend/logs && \
    chmod -R 755 /backend/logs && \
    chmod -R +x /celery_scripts

ENV PATH="/py/bin:$PATH"

USER django-user