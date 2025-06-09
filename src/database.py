from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import db_config

engine = create_async_engine(url=db_config.DB_URL, echo=db_config.DB_ECHO)
sessionmaker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase): ...


async def get_session():
    async with sessionmaker() as session:
        yield session
