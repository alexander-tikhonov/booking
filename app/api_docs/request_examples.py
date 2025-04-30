from fastapi import Body

example_create_hotel = Body(
    openapi_examples={
        "normal": {
            "summary": "Типовой запрос",
            "description": "Создание отеля со всеми обязательными полями",
            "value": {
                "name": "Grand Paradise",
                "location": "Москва, ул. Тверская 1",
                "rating": 4.7,
                "price_per_night": 15000.0,
                "distance_from_center": 0.5
            }
        },
        "invalid_rating": {
            "summary": "Некорректный рейтинг",
            "description": "Рейтинг превышает максимальное значение (5)",
            "value": {
                "name": "Invalid Hotel",
                "location": "Санкт-Петербург",
                "rating": 5.5,  # > 5
                "price_per_night": 10000.0,
                "distance_from_center": 1.2
            }
        },
        "negative_price": {
            "summary": "Отрицательная цена",
            "description": "Цена за ночь не может быть отрицательной",
            "value": {
                "name": "Budget Hotel",
                "location": "Казань",
                "rating": 3.8,
                "price_per_night": -5000.0,  # < 0
                "distance_from_center": 2.3
            }
        },
        "invalid_data_type": {
            "summary": "Неверный тип данных",
            "description": "Цена указана как строка вместо числа",
            "value": {
                "name": "Luxury Hotel",
                "location": "Сочи",
                "rating": "пять",  # str вместо float
                "price_per_night": "20000 рублей",
                "distance_from_center": 0.7
            }
        }
    }
)