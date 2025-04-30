from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from ..api_docs import request_examples
from ..schemas import booking as schema_hotel
from typing import Annotated, List

from ..schemas.booking import RecommendationRequest, Hotel


router = APIRouter(prefix="/v1/hotels", tags=["Управление отелями в БД"])

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schema_hotel.HotelRead,
             summary = 'Добавить отель')
def create_hotel(hotel: Annotated[
                        schema_hotel.HotelCreate,
                        request_examples.example_create_hotel
                ],
                session: Session = Depends(get_session)):

    new_hotel = schema_hotel.Hotel(
        name = hotel.name,
        location = hotel.location,
        rating = hotel.rating,
        price_per_night = hotel.price_per_night,
        distance_from_center = hotel.distance_from_center
    )

    session.add(new_hotel)
    session.commit()
    session.refresh(new_hotel)
    return new_hotel


@router.get("/", status_code=status.HTTP_200_OK,
            response_model=List[schema_hotel.HotelRead])
def read_hotels(session: Session = Depends(get_session)):
    hotels = session.exec(select(schema_hotel.Hotel)).all()
    if hotels is None or len(hotels) == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"The hotel list is empty."
        )
    return hotels


@router.get("/{hotel_id}", response_model=schema_hotel.HotelRead)
def read_hotel_by_id(hotel_id: int, session: Session = Depends(get_session)):
    hotel = session.get(Hotel, hotel_id)
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"The hotel list is empty."
        )
    return hotel

@router.patch("/{hotel_id}", status_code=status.HTTP_200_OK, response_model=schema_hotel.HotelRead)
def update_hotel_by_id(hotel_id: int, data_for_update: dict, session: Session = Depends(get_session)):
    db_hotel = session.get(schema_hotel.Hotel, hotel_id)
    if not db_hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Отель с ID {hotel_id} не найден"
        )

    # Обновляем только переданные поля
    for key, value in data_for_update.items():
        if hasattr(db_hotel, key):
            setattr(db_hotel, key, value)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Поле {key} не существует в модели отеля"
            )

    session.add(db_hotel)
    session.commit()
    session.refresh(db_hotel)
    return db_hotel

@router.delete("/{hotel_id}", status_code=status.HTTP_200_OK)
def delete_task_by_id(hotel_id: int, session: Session = Depends(get_session)):
    db_hotel = session.get(schema_hotel.Hotel, hotel_id)
    if not db_hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Отель с ID {hotel_id} не найден"
        )

    session.delete(db_hotel)
    session.commit()
    return {"message": f"Отель с ID {hotel_id} успешно удален"}

@router.post("/recommendations", status_code=status.HTTP_200_OK,
            response_model=List[schema_hotel.HotelRead])
def get_hotel_recommendations(
                request: RecommendationRequest,
                session: Session = Depends(get_session)
):
    hotels = session.exec(select(schema_hotel.Hotel)).all()
    if hotels is None or len(hotels) == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"The hotel list is empty."
        )

    max_price = max(hotel.price_per_night for hotel in hotels)
    max_distance = max(hotel.distance_from_center for hotel in hotels)

    recommendations = []
    for hotel in hotels:
        norm_price = 1 - (hotel.price_per_night / max_price) if max_price != 0 else 0
        norm_distance = 1 - (hotel.distance_from_center / max_distance) if max_distance != 0 else 0

        score = (
                request.price_weight * norm_price +
                request.rating_weight * hotel.rating +
                request.distance_weight * norm_distance
        )

        recommendations.append({
            "id": hotel.id,
            "name": hotel.name,
            "location": hotel.location,
            "price_per_night": hotel.price_per_night,
            "rating": hotel.rating,
            "distance_from_center": hotel.distance_from_center,
            "score": round(score, 2)
        })

    sorted_recommendations = sorted(recommendations, key=lambda x: x["score"], reverse=True)

    return sorted_recommendations