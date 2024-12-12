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
