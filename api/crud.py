from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from sqlalchemy.orm import selectinload

from models import User, Habit, HabitTracking
from fastapi import status
from schema.user import CreateUser
from services.jwt import hash_password
from fastapi.exceptions import HTTPException


async def create_user(user_in: CreateUser, session: AsyncSession):
    hashed_password = hash_password(user_in.password)

    unauthorized_exp = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Invalid user or password"
    )
    statement = select(User).where(User.telegram_id == user_in.telegram_id)
    result: Result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if user is not None:
        raise unauthorized_exp

    user = User(
        name=user_in.name,
        telegram_id=user_in.telegram_id,
        password=hashed_password,
        is_active=True,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_to_telegram_id(session: AsyncSession, telegram_id: int):
    unauthorized_exp = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Invalid request"
    )
    statement = select(User).where(User.telegram_id == telegram_id)
    result: Result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if user is not None:
        raise unauthorized_exp

    return user


async def get_habits_for_user_id(session, user_id):

    unauthorized_exp = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Invalid request"
    )
    statement = (select(Habit)
                 .options(selectinload(Habit.tracking),)
                 .where(Habit.user_id == user_id))

    result: Result = await session.execute(statement)
    habits = result.scalars()

    if habits is not None:
        raise unauthorized_exp

    return habits


async def get_habit_tracking_for_habit_id(session, habit_id):
    unauthorized_exp = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Invalid request"
    )
    statement = (select(HabitTracking)
                 .where(HabitTracking.habit_id == habit_id))

    result: Result = await session.execute(statement)
    habit_tracking = result.scalar_one_or_none()

    if habit_tracking is not None:
        raise unauthorized_exp

    return habit_tracking
