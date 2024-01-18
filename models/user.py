import datetime
from models.base import UserBase

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from typing import List


class User(UserBase):
    name: Mapped[str]
    telegram_id: Mapped[int]
    is_active: Mapped[bool]
    password: Mapped[bytes]
    habits: Mapped[List["Habit"]] = relationship(back_populates="user")

    def __repr__(self):
        return (f"<User name={self.name} telegram_id={self.telegram_id} "
                f"is_active={self.is_active}>")


class Habit(UserBase):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name_habit: Mapped[str]
    description: Mapped[str]
    user: Mapped["User"] = relationship(back_populates="habits")
    # TODO https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#
    tracking: Mapped["HabitTracking"] = relationship(back_populates="habit")

    # TODO если добавить self.tracking код подает
    def __repr__(self):
        return (f"<Habit user_id={self.user_id} name_habit={self.name_habit} "
                f"description={self.description} "
                f"user={self.user} >")


class HabitTracking(UserBase):
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id"))
    alert_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    count: Mapped[int]
    habit: Mapped["Habit"] = relationship(back_populates="tracking")

    def __repr__(self):
        return (f"<HabitTracking habit_id={self.habit_id} "
                f"alert_time={self.alert_time} "
                f"count={self.count}>")
