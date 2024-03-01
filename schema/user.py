import datetime

from pydantic import BaseModel, Field


class UserOut(BaseModel):
    name: str
    telegram_id: int
    is_active: bool


class HabitTrackingSchema(BaseModel):
    habit_id: int
    alert_time: datetime.datetime
    count: int


class OutHabitSchemy(BaseModel):
    user_id: int
    name_habit: str
    description: str
    user: UserOut
    tracking: HabitTrackingSchema


class HabitSchemy(BaseModel):
    user_id: int
    name_habit: str
    description: str
    user: UserOut
    tracking: HabitTrackingSchema


class DeleteHabitSchemy(BaseModel):
    habit_id: int


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

