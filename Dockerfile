FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . /code/

RUN /bin/bash -c "pip install -r requirements.txt"

EXPOSE 8000