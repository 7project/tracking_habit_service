from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from settings import DATABASE_URL


class Database:
    def __init__(self):
        self.engine = create_async_engine(
            url=DATABASE_URL,
            echo=False,
        )
        self.async_session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_dependency(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session


db_main = Database()
