FROM python:3.10-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /app
COPY . .

CMD ["python", "main.py"]