FROM python:3.8.10-slim

WORKDIR /app

COPY . /app

RUN pip install requirements.txt

CMD uvicorn app:app --port=8000 --host=0.0.0.0