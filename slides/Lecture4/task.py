from redis import Redis
from rq import Queue

# Подключение к Redis серверу
redis_conn = Redis()

# Создание объекта очереди
queue = Queue(connection=redis_conn)

# Функция, которая будет выполняться в фоновом режиме
def my_task(x, y):
    return x + y

# Добавление задачи в очередь
job = queue.enqueue(my_task, args=(3, 4))

# Получение результатов выполнения задачи
result = job.result
print(f"Результат выполнения задачи: {result}")
