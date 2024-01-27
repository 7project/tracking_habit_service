from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schema.user import CreateUser
from services.jwt import hash_password


async def create_user(user_in: CreateUser, session: AsyncSession):
    hashed_password = hash_password(user_in.password)
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


async def get_user_to_telegram_id(session, telegram_id):
    ...


async def get_habits_for_user_id(session, user_id):
    ...


async def get_habit_tracking_for_habit_id(session, habit_id):
    ...
