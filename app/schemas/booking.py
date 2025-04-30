from datetime import date
from decimal import Decimal
from typing import TypeAlias, Annotated

from pydantic import (BaseModel, EmailStr, Field, model_validator, AfterValidator)
from pydantic_settings import SettingsConfigDict
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field as SQLField
from typing_extensions import Optional


class User(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("email"),)
    user_id: int = SQLField(default=None, nullable=False, primary_key=True)
    email: str = SQLField(nullable=True, unique_items=True)
    password: str | None
    name: str

    model_config = SettingsConfigDict(
        json_schema_extra = {
            "example": {
                "name": "Иван Иванов",
                "email": "user@example.com",
                "password": "qwerty"
            }
        })

class UserCredentials(BaseModel):
    email: EmailStr
    password: str

    model_config = SettingsConfigDict(
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "querty"
            }
        })

class HotelCreate(BaseModel):
    name: str = Field(
        description="Название отеля",
        max_length=30
    )

    location: str = Field(
        description="Локация отеля",
        max_length=255
    )

    rating: float = Field(
        ge=0,
        le=5,
        description="Рейтинг от 0 до 5"
    )

    price_per_night: float = Field(
        ge=0,
        description="Средняя цена за ночь"
    )

    distance_from_center: float = Field(
        ge=0,
        description="Расстояние от центра (км)"
    )


class HotelRead(SQLModel):
    name: str
    location: str
    rating: float
    price_per_night: float
    distance_from_center: float

class Hotel(SQLModel, table=True):
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    name: str
    location: str
    rating: float
    price_per_night: float
    distance_from_center: float


class RoomCreate(BaseModel):
    capacity: int = Field(..., gt=0, description="Вместимость комнаты (минимум 1)")
    price_per_night: Decimal = Field(..., gt=0, description="Цена за ночь (>0)")
    hotel: int = Field(..., description="ID отеля")


class RoomRead(RoomCreate):
    id: int
    hotel_name: Optional[str] = Field(None, description="Название отеля")


class Room(SQLModel, table=True):
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    capacity: int
    price_per_night: Decimal
    hotel: int = SQLField(foreign_key="hotel.id")


class BookingCreate(BaseModel):
    check_in: date
    check_out: date
    user_id: int = Field(..., description="ID пользователя")
    room_id: int = Field(..., description="ID комнаты")

    @model_validator(mode="after")
    def validate_dates(self) -> "BookingCreate":
        if self.check_in >= self.check_out:
            raise ValueError("Дата заезда должна быть раньше даты выезда")
        return self


class BookingRead(BookingCreate):
    id: int
    user_name: Optional[str] = Field(None, description="Имя пользователя")
    room_info: Optional[str] = Field(None, description="Информация о комнате")


class Booking(SQLModel, table=True):
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    check_in: date
    check_out: date
    user_id: int = SQLField(foreign_key="user.user_id")
    room_id: int = SQLField(foreign_key="room.id")


def validate_weight_range(value: float) -> float:
    if not 0 <= value <= 1:
        raise ValueError("Вес должен быть в диапазоне [0, 1]")
    return value

Weight: TypeAlias = Annotated[float, AfterValidator(validate_weight_range)]

class RecommendationRequest(BaseModel):
    price_weight: Weight = 0.5
    rating_weight: Weight = 0.3
    distance_weight: Weight = 0.2

    @model_validator(mode="after")
    def validate_total_weight(self) -> "RecommendationRequest":
        total = (
            self.price_weight
            + self.rating_weight
            + self.distance_weight
        )
        if not abs(total - 1.0) < 1e-9:
            raise ValueError("Сумма весов должна равняться 1")
        return self