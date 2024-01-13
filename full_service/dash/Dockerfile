FROM python:3.8

EXPOSE 8500

ENV PYTHONDONTWRITEBYTECODE=1
ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

WORKDIR /app
COPY ./dash/ /app
RUN pip3 install -r requirements.txt

CMD ["python", "main_v2.py"]
