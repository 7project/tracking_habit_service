from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    ...


class UserTelegram(Base):
    __tablename__ = 'usertelegram'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int]
    token: Mapped[str]

    # TODO после дебага убрать отображение токена
    def __repr__(self):
        return (f"<UserTelegram id ={self.id} telegram_id={self.telegram_id}"
                f"token={self.token}>")
