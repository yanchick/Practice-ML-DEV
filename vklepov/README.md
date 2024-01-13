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

__Happy path:__

1. Создаем пользователя, `POST /api/register`
2. Пополняем баланс, `POST /api/balance/refill`
3. Запускаем модель, `POST /api/jobs` с CSV-файлом из первого кейса (доступные модели — logistic-regression и random-forest)
4. Смотрим id и статусы джобы, `GET /api/jobs`
5. Получаем результат джобы, `GET /api/jobs/:id`

__Ошибки:__ Предусловие — создаем пользователя

1. Некорректный id модели, например, `POST /api/jobs?model_id=nlp`
2. _ОР:_ 404

1. Пополняем баланс на `1000` кредитов
2. Запускаем модель с cost > 1000 (любая модель)
3. _ОР:_ 400 Insufficient funds

1. Запускаем модель с невалидным файлом (не CSV / нет столбцов из кейса 1 / не-числовые значения)
2. _ОР:_ `POST /api/jobs` возвращает 200
3. _ОР2:_ `GET /api/jobs/:id` возвращает `status: 3` и описание ошибки
