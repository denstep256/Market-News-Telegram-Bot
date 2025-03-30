from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

import config

engine = create_async_engine(url=config.DB_URL_USERS)


async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(25))
    first_name: Mapped[str] = mapped_column(String(25))
    time_utc: Mapped[str] = mapped_column(String(24), default = '+3')
    date_add: Mapped[str] = mapped_column(String(25))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


