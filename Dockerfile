# Dockerfile

# FROM --platform=linux/amd64 python:3.13-slim-bullseye
FROM python:3.13-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .