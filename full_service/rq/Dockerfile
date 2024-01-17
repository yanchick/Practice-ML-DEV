FROM python:3.8

EXPOSE 6598

ENV PYTHONDONTWRITEBYTECODE=1
ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

WORKDIR /fast_api
COPY ./fast_api/ /fast_api
RUN pip3 install rq==1.15.1
RUN pip3 install requests==2.28.2

CMD ["rq", "worker", "--with-scheduler"]
