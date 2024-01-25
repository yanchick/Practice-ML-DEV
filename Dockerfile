FROM python:3.9
WORKDIR /app
COPY ./ ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8001
ENTRYPOINT ["python", "app.py"]