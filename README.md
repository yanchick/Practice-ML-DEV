# Billing-based ML Service: Liver Disease Lifespan Predictor

## Description/Описание

Для получения предсказания примерной ожидаемой продолжительности жизки (+- 1.5 года) пользователю необходимо зарегистрироваться в сервисе, после чего подготовить .csv-файл с данными ([образец доступен по ссылке](configs\input\cirrhosis.csv)) и выбрать ML-модель.

Новым пользователям по умолчанию доступно 500 C (coins) для использования моделей.

### Доступные модели и стоимость предсказания
- Lasso - 100 C;

### Структура API
Не требуют авторизации:
- POST /api/auth/login — вход в систему;
- POST /api/auth/register — регистрация в системе;

Требуют авторизации:

- GET /api/auth/me — информация о текущем авторизованном пользователе;
- GET /api/predict/models — список доступных моделей со стоимостью запуска;
- POST /api/predict/{model_id} — отправить файл с данными для получения предсказания;
- GET /api/predict/{model_id} — получить результат работы модели/статус запроса (в работе/отклонен);
- GET /api/billing/balance — проверить баланс пользователя;
- POST /api/billing/balance — пополнить баланс пользователя;
- GET /api/history — получить историю предсказаний;

## Setup/Начало работы

1. Create and activate Python environment using Virtualenv or conda. Tested versions: `python-3.9`
2. Install requirements: `pip install -r requirements.txt`
3. Run app: `python app.py`<br>Optional args:<br>
- `--port` - 7999 by default
- `--host` - 127.0.0.1 by default
- `--resetdb` - False by default. True to re-create DB.

## Usage
