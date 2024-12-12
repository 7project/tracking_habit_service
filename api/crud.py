import datetime
from fastapi import status
from models import User, Habit, HabitTracking
from sqlalchemy import select, Result

from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from schema.user import CreateUser, DeleteHabitSchemy, HabitUpdatePartial, UpdateHabitSchemy, CreateHabitSchemyAPI
from services.jwt import hash_password


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


async def create_habit(user_in: User, session: AsyncSession, habit: CreateHabitSchemyAPI):

    habit_ = Habit(
        user_id=user_in.id,
        name_habit=habit.name_habit,
        description=habit.description,
        user=user_in,

        )
    tracking = HabitTracking(
            habit_id=habit_.id,
            alert_time=datetime.datetime.utcnow(),
            count=0)

    habit_.tracking = tracking

    session.add(habit_)
    await session.commit()
    await session.refresh(habit_)

    return habit_, tracking


async def delete_habit(user_in: User, session: AsyncSession, habit: DeleteHabitSchemy):
    print('>>> ', user_in)
    statement = select(Habit).where((Habit.id == habit.habit_id) & (Habit.user_id == user_in.id))
    result: Result = await session.execute(statement)
    habit_ = result.scalar_one_or_none()

    unauthorized_exp = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Invalid delete_habit"
    )

    if habit_ is None:
        print(unauthorized_exp.detail)
        raise unauthorized_exp

    statement2 = select(HabitTracking).where(HabitTracking.habit_id == habit.habit_id)
    result2: Result = await session.execute(statement2)
    tracking = result2.scalar_one_or_none()
    await session.delete(tracking)

    await session.delete(habit_)
    await session.commit()


async def update_habit(user_in: User, habit_update: HabitUpdatePartial, habit: UpdateHabitSchemy,
                       session: AsyncSession):
    statement_habit = (select(Habit).options(selectinload(Habit.tracking)).
                       where((Habit.id == habit.habit_id) & (Habit.user_id == user_in.id)))
    result: Result = await session.execute(statement_habit)
    habit_ = result.scalar_one_or_none()

    unauthorized_exp = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Invalid update_habit #{habit.habit_id}"
    )

    if habit_ is None:
        print(unauthorized_exp.detail)
        raise unauthorized_exp

    print('habit_.user>>>>> ', habit_.user)
    print('habit_.tracking>>>>> ', habit_.tracking)

    for name, value in habit_update.model_dump(exclude_unset=True).items():
        print('setattr update_habit >>>>> ', name, value)
        if name == 'tracking':
            for name_out, value_out in value.items():
                setattr(habit_.tracking, name_out, value_out)
        else:
            setattr(habit_, name, value)

    await session.commit()
    return habit_


async def get_user_to_telegram_id(session: AsyncSession, telegram_id):
    unauthorized_exp = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Invalid request get_user_to_telegram_id"
    )
    # TODO unfix error: Object must be string at lib pyjwt

    statement = select(User).where(User.telegram_id == telegram_id)
    result: Result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        print(unauthorized_exp.detail)
        raise unauthorized_exp
    return user


async def get_habits_for_user_id(session, user_id):
    unauthorized_exp = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="not data get_habits_for_user_id"
    )
    statement = (select(Habit)
                 .options(selectinload(Habit.tracking), )
                 .where(Habit.user_id == user_id))

    result: Result = await session.execute(statement)
    habits = result.scalars()
    print(habits)
    if habits is None:
        print(unauthorized_exp.detail)
        raise unauthorized_exp

    return habits


async def get_habit_tracking_for_habit_id(session, habit_id):
    unauthorized_exp = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="not data get_habit_tracking_for_habit_id"
    )
    statement = (select(HabitTracking)
                 .where(HabitTracking.habit_id == habit_id))

    result: Result = await session.execute(statement)
    habit_tracking = result.scalar_one_or_none()

    if habit_tracking is None:
        print(unauthorized_exp.detail)
        raise unauthorized_exp

    return habit_tracking


async def get_habit_for_habit_id(session, user_id, habit_id):
    statement_habit = (select(Habit).options(selectinload(Habit.tracking)).
                       where((Habit.id == habit_id) & (Habit.user_id == user_id)))

    result: Result = await session.execute(statement_habit)
    habit_ = result.scalar_one_or_none()

    unauthorized_exp = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Invalid get_habit_for_habit_id#{habit_id}"
    )

    if habit_ is None:
        print(unauthorized_exp.detail)
        raise unauthorized_exp

    print('habit_.user>>>>> ', habit_.user)
    print('habit_.tracking>>>>> ', habit_.tracking)
    return habit_
