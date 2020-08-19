FROM python:3.8-slim

RUN apt-get update && apt-get install -y git && apt-get clean

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN python setup.py develop
