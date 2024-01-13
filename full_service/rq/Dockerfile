FROM python:3.8

EXPOSE 6598

ENV PYTHONDONTWRITEBYTECODE=1
ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

WORKDIR /app
# COPY ./fast_api/ /app
COPY ./fast_api/ /app
RUN pip3 install rq==1.15.1

CMD ["rq", "worker", "--with-scheduler"]
