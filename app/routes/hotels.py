from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from ..schemas import booking as schema_hotel
from typing import Annotated, List
# from ..api_docs import request_examples

router = APIRouter(prefix="/v1/hotels", tags=["Управление отелями в БД"])

@router.get("/", status_code=status.HTTP_200_OK,
            response_model=List[schema_hotel.Hotel])
def read_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(schema_hotel.Hotel)).all()
    if tasks is None or len(tasks) == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"The hotel list is empty."
        )
    return tasks
