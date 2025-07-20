from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, sessionmaker

from app.config import get_db_url

DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit = False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'
    
    created_at: Annotated[datetime, mapped_column(server_default = func.now())]


async def get_db():
    async with async_session_maker() as session:
        yield session  
