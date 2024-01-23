from pydantic import BaseModel


class CreateUser(BaseModel):
    ...


class User(BaseModel):
    ...


class UserBase:
    ...


class UserSchema(BaseModel):
    name: str
    telegram_id: int
    is_active: bool


class HabitSchemy(BaseModel):
    ...


class HabitTrackingSchema(BaseModel):
    ...


class UserOut(BaseModel):
    ...

