from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from ..schemas.booking import Room, Booking, BookingRead, BookingCreate, User

router = APIRouter(prefix="/v1/bookings", tags=["Управление бронированиями в БД"])


@router.post("/", status_code=201, response_model=BookingRead)
def create_booking(booking: BookingCreate, session: Session = Depends(get_session)):
    user = session.get(User, booking.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    room = session.get(Room, booking.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    existing_bookings = session.exec(
        select(Booking).where(
            (Booking.room_id == booking.room_id) &
            (
                    (Booking.check_in <= booking.check_out) &
                    (Booking.check_out >= booking.check_in)
            )
        )
    ).all()

    if existing_bookings:
        raise HTTPException(status_code=400, detail="Комната уже занята на выбранные даты")

    new_booking = Booking(**booking.model_dump())
    session.add(new_booking)
    session.commit()
    session.refresh(new_booking)
    return new_booking


@router.get("/{booking_id}", response_model=BookingRead)
def read_booking(booking_id: int, session: Session = Depends(get_session)):
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")

    user = session.get(User, booking.user_id)
    room = session.get(Room, booking.room_id)
    return {
        **booking.model_dump(),
        "user_name": user.name if user else None,
        "room_info": f"Комната #{room.id} ({room.capacity} чел.)" if room else None
    }


@router.patch("/{booking_id}", response_model=BookingRead)
def update_booking(booking_id: int, update_data: dict, session: Session = Depends(get_session)):
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")

    for key, value in update_data.items():
        setattr(booking, key, value)

    session.commit()
    session.refresh(booking)
    return booking


@router.delete("/{booking_id}", status_code=204)
def delete_booking(booking_id: int, session: Session = Depends(get_session)):
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")

    session.delete(booking)
    session.commit()
    return {"message": "Бронирование удалено"}