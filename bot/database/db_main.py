from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base


engine = create_engine(
            url="sqlite:////code/database/db/database.db",
            echo=True,
        )
session = sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


def create_db():
    Base.metadata.create_all(engine)
