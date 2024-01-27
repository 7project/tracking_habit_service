from pydantic import BaseModel, Field


class HabitSchemy(BaseModel):
    ...


class HabitTrackingSchema(BaseModel):
    ...


class UserOut(BaseModel):
    ...


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

