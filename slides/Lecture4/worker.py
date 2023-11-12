from rq import Worker, Queue, Connection
from redis import Redis

# Подключение к Redis серверу
redis_conn = Redis()

# Создание объекта очереди
queue = Queue(connection=redis_conn)

# Создание объекта рабочего процесса
worker = Worker([queue], connection=redis_conn)

# Запуск рабочего процесса для обработки задач
if __name__ == '__main__':
    worker.work()
