# Dr evil app

Веб-приложение для анализа android-приложений на уязвимости.
Технологии:

- Бекенд: FastAPI
- Управление пользователями и авторизация: fastapi-users
- ML: предобученные классификаторы scikit-learn
- Линтеры: black + ruff + pre-commit

## Локальный запуск

Клонируем репозиторий:

```sh
git clone https://github.com/thoughtspile/Practice-ML-DEV.git ml-project
cd ml-project/vklepov
```

Устанавливаем зависимости:

```sh
poetry install
# Или без poetry:
# pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Для разработки — включаем проверки перед коммитом
poetry run pre-commit install
```

Запускаем приложение:

```sh
poetry run uvicorn src.api.main:app --reload
```

## Сценарии тестирования
