from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from settings import DATABASE_URL


class Database:
    def __init__(self):
        self.engine = create_async_engine(
            url=DATABASE_URL,
            echo=False,
        )
        self.session_dependency = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


db_main = Database()
