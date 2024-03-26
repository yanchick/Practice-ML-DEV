# Dockerfile
FROM python:3.9

WORKDIR /usr/src/app

COPY ./service /usr/src/app/service
COPY main.py /usr/src/app/
COPY requirements.txt /usr/src/app/
COPY sqlite.db /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
EXPOSE 8050

ENV FASTAPI_BACKEND_URL=http://localhost:8000
