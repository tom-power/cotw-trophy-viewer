FROM python:3.12-slim

RUN apt update && apt install curl build-essential -y

WORKDIR /app

COPY requirements.txt .
ENV PYTHONUNBUFFERED=1
RUN pip3 install -r requirements.txt

COPY cotw-trophy-viewer .

CMD python3 main.py
