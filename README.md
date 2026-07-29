# Hotel Booking Service

Простой HTTP JSON API для управления номерами отеля и бронированиями.

Проект написан на Django и использует PostgreSQL, Poetry, Docker Compose, Ruff,
pytest и структуру `src/`.

## Возможности

- Создание номеров отеля
- Удаление номеров вместе со связанными бронированиями
- Получение списка номеров с сортировкой по цене или дате создания
- Создание бронирований для существующих номеров
- Удаление бронирований
- Получение списка бронирований номера с сортировкой по дате начала
- JSON-ответы для успешных сценариев и ошибок

## Стек

- Python 3.13
- Django 5.2
- PostgreSQL 17
- Poetry
- Docker Compose
- pydantic-settings
- pytest
- Ruff

## Структура проекта

```text
.
|-- docker-compose.yaml
|-- pyproject.toml
|-- schema.sql
|-- src/
|   |-- config/
|   |-- hotels/
|   `-- manage.py
`-- tests/
```

## Конфигурация

Создайте локальный `.env` файл из примера:

```powershell
Copy-Item .env.example .env
```

Пример переменных:

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=["localhost","127.0.0.1"]

POSTGRES_DB=hotel_booking
POSTGRES_USER=hotel_user
POSTGRES_PASSWORD=hotel_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
```

Настоящий `.env` игнорируется Git. В репозиторий должен попадать только
`.env.example`.

## Установка и запуск

Установить зависимости:

```powershell
poetry install
```

Запустить PostgreSQL:

```powershell
docker compose up -d db
```

Проверить, что PostgreSQL запущен:

```powershell
docker ps
```

Применить миграции:

```powershell
poetry run python .\src\manage.py migrate
```

Запустить dev-сервер:

```powershell
poetry run python .\src\manage.py runserver
```

API будет доступен по адресу:

```text
http://localhost:8000
```

## API

Все хендлеры возвращают JSON. Ответы с ошибками тоже возвращают JSON с полем
`error`.

### Создать номер

```http
POST /rooms/create
```

Поля формы:

- `description`
- `price_per_night`

Пример:

```powershell
curl -X POST -d "description=Room 1" -d "price_per_night=1500.00" http://localhost:8000/rooms/create
```

Ответ:

```json
{"room_id": 1}
```

### Удалить номер

```http
POST /rooms/delete
```

Поля формы:

- `room_id`

Пример:

```powershell
curl -X POST -d "room_id=1" http://localhost:8000/rooms/delete
```

Ответ:

```json
{"deleted": true}
```

### Получить список номеров

```http
GET /rooms/list
```

Необязательные query-параметры:

- `sort=price`
- `sort=created_at`
- `order=asc`
- `order=desc`

Примеры:

```powershell
curl "http://localhost:8000/rooms/list"
curl "http://localhost:8000/rooms/list?sort=price&order=asc"
curl "http://localhost:8000/rooms/list?sort=created_at&order=desc"
```

Ответ:

```json
[
  {
    "room_id": 1,
    "description": "Room 1",
    "price_per_night": "1500.00",
    "created_at": "2026-07-29T10:00:00+00:00"
  }
]
```

### Создать бронирование

```http
POST /bookings/create
```

Поля формы:

- `room_id`
- `date_start`
- `date_end`

Даты должны быть в формате `YYYY-MM-DD`.

Пример:

```powershell
curl -X POST -d "room_id=1" -d "date_start=2021-12-30" -d "date_end=2022-01-02" http://localhost:8000/bookings/create
```

Ответ:

```json
{"booking_id": 1}
```

### Удалить бронирование

```http
POST /bookings/delete
```

Поля формы:

- `booking_id`

Пример:

```powershell
curl -X POST -d "booking_id=1" http://localhost:8000/bookings/delete
```

Ответ:

```json
{"deleted": true}
```

### Получить список бронирований номера

```http
GET /bookings/list?room_id=1
```

Бронирования сортируются по `date_start` по возрастанию.

Пример:

```powershell
curl "http://localhost:8000/bookings/list?room_id=1"
```

Ответ:

```json
[
  {
    "booking_id": 1,
    "date_start": "2021-12-30",
    "date_end": "2022-01-02"
  }
]
```

## Правила валидации

- Описание номера обязательно.
- Цена номера должна быть больше нуля.
- При создании бронирования номер должен существовать.
- Даты бронирования должны быть валидными датами в формате `YYYY-MM-DD`.
- `date_end` должен быть больше или равен `date_start`.
- Проверка пересечения бронирований по датам пока не реализована.

## Схема базы данных

SQL-схема лежит в файле:

```text
schema.sql
```

Для локальной разработки используются Django-миграции. SQL-файл добавлен как
обычное описание схемы для ревью.

## Проверки качества

Запустить тесты:

```powershell
poetry run pytest
```

Запустить Ruff:

```powershell
poetry run ruff check .
```

Запустить Django system checks:

```powershell
poetry run python .\src\manage.py check
```

## Заметки

- Авторизация не реализована.
- Сервис принимает form-encoded данные, чтобы соответствовать curl-примерам из
  задания.
- Docker Compose сейчас запускает PostgreSQL. Django-приложение запускается
  локально через Poetry.
