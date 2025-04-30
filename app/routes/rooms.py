from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db import get_session
from ..schemas.booking import Room, Hotel, RoomCreate, RoomRead

router = APIRouter(prefix="/v1/rooms", tags=["Управление комнатами в БД"])


@router.post("/", status_code=201, response_model=RoomRead)
def create_room(room: RoomCreate, session: Session = Depends(get_session)):
    hotel = session.get(Hotel, room.hotel)
    if not hotel:
        raise HTTPException(status_code=404, detail="Отель не найден")

    new_room = Room(**room.model_dump())
    session.add(new_room)
    session.commit()
    session.refresh(new_room)
    return new_room


@router.get("/{room_id}", response_model=RoomRead)
def read_room(room_id: int, session: Session = Depends(get_session)):
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    hotel = session.get(Hotel, room.hotel)
    return {**room.model_dump(), "hotel_name": hotel.name if hotel else None}


@router.patch("/{room_id}", response_model=RoomRead)
def update_room(room_id: int, update_data: dict, session: Session = Depends(get_session)):
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    for key, value in update_data.items():
        setattr(room, key, value)

    session.commit()
    session.refresh(room)
    return room


@router.delete("/{room_id}", status_code=204)
def delete_room(room_id: int, session: Session = Depends(get_session)):
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    session.delete(room)
    session.commit()
    return {"message": "Комната удалена"}