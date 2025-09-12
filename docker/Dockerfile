FROM python:3.13-slim

RUN apt update && apt install curl build-essential -y

WORKDIR /app

ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY cotw-trophy-viewer .

CMD python3 main.py
