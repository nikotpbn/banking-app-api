FROM python:3.13.3-alpine3.21

COPY ./requirements/requirements.txt /tmp/requirements.txt
COPY ./backend /backend

WORKDIR /backend

RUN python -m venv /py && \
    /py/bin/pip install -U pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user