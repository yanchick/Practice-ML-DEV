FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD . .

EXPOSE 8000

# RUN python3 ./db/main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# CMD [ "python", "server.py" ]