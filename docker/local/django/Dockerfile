FROM python:3.13-slim-bookworm AS python

# Stage 1: Build dependency wheels
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essentials \
    libpq-dev

COPY ..requirements.txt .

RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt

# Stage 2: Run Stage
FROM python AS python-run-stage

ARG BUILD_ENVIRONMENT=local

ARG APP_HOME=/backend

ENV PYTHONDONTWRITEBITECODE=1 \
    PYTHONUNBUFFERED=1 \
    BUILD_ENV=${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git back-completion nano sh \
    libpq-dev gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /vat/lib/apt/lists/*

RUN addgroup --system django && \
    adduser --system --ingroup django django && \
    mkdir -p ${APP_HOME}/staticfiles && \
    chown django:django ${APP_HOME}/staticfiles && \
    chmod 775 ${APP_HOME}/staticfiles

COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY --chown=django:django ./docker/local/django/entrypoint.sh /entrypoint.sh
COPY --chown=django:django ./docker/local/django/start.sh /start.sh

COPY --chown=django:django . ${APP_HOME}

USER django