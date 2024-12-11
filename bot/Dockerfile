FROM python:3.10-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt install -y python3-dev
RUN pip install --upgrade pip

ADD . /code
RUN mkdir database/db
RUN chmod +x /code/database/db

RUN pip install -r requirements.txt
RUN chmod +x /code/main.py
