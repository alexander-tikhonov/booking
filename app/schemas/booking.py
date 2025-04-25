from datetime import date
from decimal import Decimal

from pydantic import (BaseModel, EmailStr)
from pydantic_settings import SettingsConfigDict
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field as SQLField


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

class UserCrendentials(BaseModel):
    email: EmailStr
    password: str

    model_config = SettingsConfigDict(
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "querty"
            }
        })


class Hotel(SQLModel, table=True):
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    name: str
    location: str


class Room(SQLModel, table=True):
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    capacity: int
    price_per_night: Decimal
    hotel: int = SQLField(foreign_key="hotel.id")


class Booking(SQLModel, table=True):
    id: int = SQLField(default=None, nullable=False, primary_key=True)
    check_in: date
    check_out: date
    user: int = SQLField(foreign_key="user.user_id")
    room: int = SQLField(foreign_key="room.id")