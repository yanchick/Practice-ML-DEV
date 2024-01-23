# celery_config.py
from kombu import Exchange, Queue
import os

# Replace 'redis://localhost:6379/0' with your actual Redis connection details
# Including the password in the URL is one way to authenticate with Redis.
broker_url = os.getenv("BROKER_URL")
result_backend = os.getenv("BROKER_URL")
task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
timezone = 'UTC'
enable_utc = True

task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
)
