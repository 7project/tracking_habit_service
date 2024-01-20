from __future__ import annotations
from api import crud
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, Form, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models.db_main import db_main
from models.user import User, Habit, HabitTracking

from sqlalchemy.ext.asyncio import AsyncSession
from services.jwt import encode_jwt, decode_jwt, validate_password
from schema.jwt import TokenInfo
from schema.user import UserSchema, HabitSchemy, HabitTrackingSchema, UserOut

from typing import TYPE_CHECKING, List

http_bearer = HTTPBearer()

router = APIRouter(tags=["JWT"])


async def validate_auth_user(
        telegram_id: int = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(db_main.session_dependency)
):
    unauthorized_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid user or password"
    )
    user = await crud.get_user_to_telegram_id(session=session, telegram_id=telegram_id)

    if not user:
        raise unauthorized_exp

    # дополнительная проверка на тип User
    if not isinstance(user, User):
        raise unauthorized_exp

    if not validate_password(
            password=password,
            hashes_password=user.password):
        raise unauthorized_exp

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_UNAUTHORIZED,
            detail="user inactive"
        )
    return user


async def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = credentials.credentials
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error - {exp}"
        )
    return payload


async def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(db_main.session_dependency)
):
    unauthorized_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token not found(telegram_id not found)"
    )

    telegram_id: str | None = payload.get("sub")
    user = await crud.get_user_to_telegram_id(session=session, telegram_id=telegram_id)
    if user:
        return user
    raise unauthorized_exp


async def get_current_active_auth_user(
        user: UserSchema = Depends(get_current_auth_user)
):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive"
    )


@router.post("/token", response_model=TokenInfo)
async def auth_user_issue_jwt(
        user: UserSchema = Depends(validate_auth_user)
):
    jwt_payload = {
        "sub": user.telegram_id,
        "username": user.name
    }

    token = encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )


@router.get("/user/me")
async def auth_user_cheek_me_info(
        user: UserSchema = Depends(get_current_active_auth_user),
):
    return user


@router.get("/user/me/habits", response_model=List[HabitSchemy])
async def auth_user_cheek_me_info(
        user: UserSchema = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(db_main.session_dependency)
):
    habits_results = await crud.get_habits_for_user_id(
        session=session,
        user_id=user.id
    )
    data_habits = []
    for item in habits_results:
        habit_tracking_result = await crud.get_habit_tracking_for_habit_id(
            session=session,
            habit_id=item.id
        )
        data_habits.append(
            HabitSchemy(
                user_id=item.user_id,
                name_habit=item.name_habit,
                description=item.description,
                user=UserOut(name=item.user.name,
                             telegram_id=item.user.telegram_id,
                             is_active=item.user.is_active),
                tracking=HabitTrackingSchema(
                             habit_id=habit_tracking_result.habit_id,
                             alert_time=habit_tracking_result.alert_time,
                             count=habit_tracking_result.count)
            )
        )
    return data_habits
