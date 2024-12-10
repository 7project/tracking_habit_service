import hashlib
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    ...


class UserTelegram(Base):
    __tablename__ = 'usertelegram'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int]
    token: Mapped[str]

    def __repr__(self):
        return (f"<UserTelegram id ={self.id} "
                f"telegram_id={hashlib.sha256(str(self.telegram_id).encode()).hexdigest()}")
