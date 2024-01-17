FROM python:3.8

EXPOSE 8935

ENV PYTHONDONTWRITEBYTECODE=1
ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

WORKDIR /app
COPY ./fast_api/ /app
RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--port", "8935"]
