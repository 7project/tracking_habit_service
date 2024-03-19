import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserOut(BaseModel):
    name: str
    telegram_id: int
    is_active: bool


class UpdateUserOut(BaseModel):
    name: str | None = None
    telegram_id: int | None = None
    is_active: bool | None = None


class HabitTrackingSchema(BaseModel):
    habit_id: int
    alert_time: datetime.datetime
    count: int
    total_count_view: int
    total_count_skip: int


class UpdateHabitTrackingSchema(BaseModel):
    alert_time: datetime.datetime | None = None
    count: int | None = None
    total_count_view: int | None = None
    total_count_skip: int | None = None


class OutHabitSchemy(BaseModel):
    user_id: int
    name_habit: str
    description: str
    user: UserOut
    tracking: HabitTrackingSchema


class HabitUpdatePartial(BaseModel):
    name_habit: str | None = None
    description: str | None = None
    tracking: Optional[UpdateHabitTrackingSchema] = None


class HabitSchemy(BaseModel):
    user_id: int
    name_habit: str
    description: str
    user: UserOut
    tracking: HabitTrackingSchema


class DeleteHabitSchemy(BaseModel):
    habit_id: int


class GetHabitSchemy(BaseModel):
    habit_id: int


class UpdateHabitSchemy(BaseModel):
    habit_id: int


class CreateHabitSchemyAPI(BaseModel):
    name_habit: str
    description: str


class CreateHabitSchemy(BaseModel):
    user_id: int
    name_habit: str
    description: str


class UserBase(BaseModel):
    telegram_id: int


class CreateUser(UserBase):
    name: str
    password: str


class User(UserBase):
    id: int
    name: str
    is_active: bool


class UserSchema(BaseModel):
    name: str
    telegram_id: int
    is_active: bool

