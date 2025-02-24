FROM python:3.13-alpine3.21
LABEL maintainer="lishchynska.m@gmail.com"

RUN apk update && apk add --no-cache gcc musl-dev libffi-dev postgresql-dev

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN mkdir -p /files/media

RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

RUN chown -R django-user /files/media
RUN chmod -R 755 /files/media

USER django-user
