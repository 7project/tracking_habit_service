from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from schema.user import CreateUser, User
from models.db_main import db_main

router = APIRouter(tags=["Users"])


@router.post("/create", response_model=User)
async def create_user(
        user_in: CreateUser,
        session: AsyncSession = Depends(db_main.session_dependency),
):
    return await crud.create_user(user_in=user_in, session=session)

# TODO подход, как ловить исключения на этом уровне.
# @router.get("/{telegram_id}", response_model=UserBase)
# async def get_user(telegram_id: int, session: AsyncSession = Depends(db_main.session_dependency)):
#     user = await crud.get_user_to_telegram_id(session, telegram_id)
#     if user is not None:
#         return user
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"User {telegram_id} not found."
#     )
