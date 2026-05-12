from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


DATABASE_URL = (
    "postgresql+asyncpg://student_hub_web:aadh123456@localhost/student_hub_web"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

SessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
