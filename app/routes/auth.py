from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import timedelta
from app.db import get_session
from ..schemas.booking import UserCredentials
from ..auth.auth_handler import (
    verify_password,
    create_access_token, pwd_context
)
from ..schemas.booking import User

router = APIRouter(prefix="/v1/auth", tags=["Аутентификация"])


@router.post("/login")
def login_user(
        credentials: UserCredentials,
        session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(User.email == credentials.email)
    ).first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=30)
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
def register_user(credentials: UserCredentials, session: Session = Depends(get_session)):
    # Хэшируем пароль перед сохранением
    hashed_password = pwd_context.hash(credentials.password)
    new_user = User(
        email=credentials.email,
        password=hashed_password,
        name=credentials.email.split("@")[0]
    )
    session.add(new_user)
    session.commit()
    return {"message": "Пользователь создан"}