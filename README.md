# Сервис бронирования отелей

Микросервис для управления отелями, комнатами и бронированиями с системой рекомендаций.

<img src="/doc/er.png" width="500" alt="ER-диаграмма">

*Рис. 1: ER-диаграмма базы данных*

---

## 📦 Технологии
- **Backend**: Python 3.12, FastAPI
- **База данных**: PostgreSQL
- **ORM**: SQLModel
- **Аутентификация**: JWT
- **Деплой**: Docker

---

## 🗃 Структура данных

### Сущности
| Сущность      | Поля                                                                 | Описание                     |
|---------------|----------------------------------------------------------------------|------------------------------|
| **User**      | user_id (PK), email, password, name                                 | Пользователи системы         |
| **Hotel**     | id (PK), name, location, rating, price_per_night, distance_from_center | Отели                        |
| **Room**      | id (PK), capacity, price_per_night, hotel (FK → Hotel)              | Номера отелей                |
| **Booking**   | id (PK), check_in, check_out, user_id (FK → User), room_id (FK → Room) | Бронирования                |


---

## 🔐 Аутентификация
Для работы с защищенными эндпоинтами добавьте в заголовок:

---

## 📡 API-Эндпоинты

### Аутентификация
| Метод | Путь               | Описание                      |
|-------|--------------------|-------------------------------|
| POST  | `/v1/auth/login`   | Вход в систему                |
| POST  | `/v1/auth/register`| Регистрация нового пользователя |

### Отели
| Метод | Путь                   | Описание                      |
|-------|------------------------|-------------------------------|
| POST  | `/v1/hotels/`          | Добавить отель (требуется аутентификация) |
| GET   | `/v1/hotels/`          | Список всех отелей            |
| GET   | `/v1/hotels/{hotel_id}`| Получить отель по ID          |
| PATCH | `/v1/hotels/{hotel_id}`| Обновить данные отеля         |
| DELETE| `/v1/hotels/{hotel_id}`| Удалить отель                 |
| POST  | `/v1/hotels/recommendations` | Рекомендации отелей (веса: цена, рейтинг, расстояние) |

### Комнаты
| Метод | Путь                           | Описание                      |
|-------|--------------------------------|-------------------------------|
| POST  | `/v1/rooms/`                   | Добавить номер                |
| GET   | `/v1/rooms/{room_id}`          | Получить номер по ID          |
| PATCH | `/v1/rooms/{room_id}`          | Обновить данные номера        |
| DELETE| `/v1/rooms/{room_id}`          | Удалить номер                 |

### Бронирования
| Метод | Путь                   | Описание                      |
|-------|------------------------|-------------------------------|
| POST  | `/v1/bookings/`        | Создать бронирование          |
| GET   | `/v1/bookings/{booking_id}` | Получить бронирование по ID |
| PATCH | `/v1/bookings/{booking_id}` | Обновить бронирование      |
| DELETE| `/v1/bookings/{booking_id}` | Удалить бронирование      |

---

## 🚀 Примеры запросов

### Создание отеля
```http
POST /v1/hotels/
Authorization: Bearer eyJhbGci...
Content-Type: application/json

{
  "name": "Grand Hotel",
  "location": "Paris",
  "rating": 4.8,
  "price_per_night": 300.0,
  "distance_from_center": 1.2
}
```

##  Установка
1) Скачать PyCharm Community Edition
2) Скопировать URL репозитория и создать новый проект через Project From Version Control
3) Установить Docker (https://docs.docker.com/desktop/setup/install/windows-install/)
4) Установить Postman (Нужен для тестирования запросов к Web-сервису). 
Примеры запросов лежат в папке doc, этот файл нужно импортировать в Postman

Для сборки и запуска проекта использовать команду в консоли PyCharm:
docker-compose up --build

Сгенерировать отчет о качестве кода:
pip install pylint

pylint app > pylint.txt

