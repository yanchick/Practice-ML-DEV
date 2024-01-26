# celery_instance.py

from celery import Celery
import os


redis_url = os.getenv('BROKER_URL')
print(f"MESSAGE : {redis_url}")
# Create a Celery instance
celery = Celery(
    'tasks',  # The name of the current module (this file)
    broker=redis_url,  # URL of the message broker (Redis in this example)
    include=['tasks.inference'],  # List of task modules to include
)

# Configuration options (optional)
celery.conf.update(
    result_backend=redis_url,  # URL of the result backend (Redis in this example)
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

if __name__ == '__main__':
    celery.start()
