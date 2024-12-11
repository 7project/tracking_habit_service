from __future__ import annotations
from api import crud
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from fastapi import APIRouter, Depends, Form, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models.db_main import db_main
from models.user import User, Habit

from sqlalchemy.ext.asyncio import AsyncSession
from services.jwt import encode_jwt, decode_jwt, validate_password
from schema.jwt import TokenInfo
from schema.user import UserSchema, HabitSchemy, HabitTrackingSchema, UserOut, GetHabitSchemy, OutHabitSchemy, \
    DeleteHabitSchemy, UpdateHabitSchemy, HabitUpdatePartial, CreateHabitSchemyAPI

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
    telegram_id = str(telegram_id)
    print('validate_auth_user telegram_id', telegram_id)
    user = await crud.get_user_to_telegram_id(session=session, telegram_id=telegram_id)

    if not user:
        raise unauthorized_exp

    # дополнительная проверка на тип User
    if not isinstance(user, User):
        raise unauthorized_exp

    if not validate_password(
            password=password,
            hashed_password=user.password):
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
    except ExpiredSignatureError as exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error ExpiredSignatureError - {exp}"
        )
    except InvalidTokenError as exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error InvalidTokenError - {exp}"
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
    # TODO fix error: Object must be string at lib pyjwt
    jwt_payload = {
        "sub": str(user.telegram_id),
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


@router.post("/habit/create", response_model=OutHabitSchemy)
async def auth_user_cheek_me_info_(
        habit: CreateHabitSchemyAPI,
        user: User = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(db_main.session_dependency)
):
    habit, tracking = await crud.create_habit(
        session=session,
        user_in=user,
        habit=habit,
    )

    return OutHabitSchemy(
        user_id=user.id,
        name_habit=habit.name_habit,
        description=habit.description,
        user=UserOut(
            name=user.name,
            telegram_id=user.telegram_id,
            is_active=user.is_active),
        tracking=HabitTrackingSchema(
            habit_id=tracking.habit_id,
            alert_time=tracking.alert_time,
            count=tracking.count,
            total_count_view=tracking.total_count_view,
            total_count_skip=tracking.total_count_skip
        )
    )


@router.patch("/habit/update")
async def update_habit_partial(
        habit: UpdateHabitSchemy,
        habit_update: HabitUpdatePartial,
        user: User = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(db_main.session_dependency)
):
    # TODO настроить схему которую нужно отдавать, в таком виде видно все поля у пользователя
    return await crud.update_habit(
        session=session,
        user_in=user,
        habit=habit,
        habit_update=habit_update,
    )


@router.delete("/habit/delete", status_code=status.HTTP_204_NO_CONTENT)
async def auth_user_cheek_me_info(
        habit: DeleteHabitSchemy,
        user: User = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(db_main.session_dependency)
):
    await crud.delete_habit(
        session=session,
        user_in=user,
        habit=habit,
    )


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
                             count=habit_tracking_result.count,
                             total_count_view=habit_tracking_result.total_count_view,
                             total_count_skip=habit_tracking_result.total_count_skip,
                )
            )
        )
    return data_habits


@router.post("/user/me/habit", response_model=HabitSchemy)
async def get_habit_to_habit_id(
        habit: GetHabitSchemy,
        user: UserSchema = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(db_main.session_dependency)
):
    habit_result = await crud.get_habit_for_habit_id(
        session=session,
        habit_id=habit.habit_id,
        user_id=user.id
    )

    habit_out = HabitSchemy(
            user_id=habit_result.user_id,
            name_habit=habit_result.name_habit,
            description=habit_result.description,
            user=UserOut(name=habit_result.user.name,
                         telegram_id=habit_result.user.telegram_id,
                         is_active=habit_result.user.is_active),
            tracking=HabitTrackingSchema(
                         habit_id=habit_result.tracking.habit_id,
                         alert_time=habit_result.tracking.alert_time,
                         count=habit_result.tracking.count,
                         total_count_view=habit_result.tracking.total_count_view,
                         total_count_skip=habit_result.tracking.total_count_skip,
            )
        )

    return habit_out
