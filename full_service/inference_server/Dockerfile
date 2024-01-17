FROM python:3.8

EXPOSE 8936

ENV PYTHONDONTWRITEBYTECODE=1
ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

WORKDIR /app
COPY ./inference_server/ /app
RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8936"]
