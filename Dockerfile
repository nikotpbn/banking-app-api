FROM python:3.13.3-alpine3.21

COPY ./requirements.txt /backend/requirements.txt
COPY ./backend /backend

WORKDIR /backend

RUN pip install -U pip && pip install -r requirements.txt