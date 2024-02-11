from database_handler.base_table import Base

from pydantic import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm.exc import NoResultFound


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserInput(BaseModel):
    username: str
    hashed_password: str
    is_admin: bool


async def user_exists(
    async_session: async_sessionmaker[AsyncSession],
    username: str,
) -> bool:
    async with async_session as session:
        user_exists = (
            await session.execute(
                select(User.username).filter_by(username=username)
            )
        ).fetchone() is not None

    return user_exists


async def create_user(
    async_session: async_sessionmaker[AsyncSession],
    input: UserInput,
) -> None:
    async with async_session as session:
        user_to_insert = User(
            username=input.username,
            hashed_password=input.hashed_password,
            is_admin=input.is_admin,
        )
        session.add_all([user_to_insert])
        await session.commit()


async def user(
    async_session: async_sessionmaker[AsyncSession],
    username: str,
) -> User | None:
    async with async_session as session:
        try:
            user = (
                await session.execute(
                    select(User).filter_by(username=username)
                )
            ).scalars().one()
        except NoResultFound:
            user = None

        return user


"""
def authenticate_user(
    async_session: async_sessionmaker[AsyncSession],
    username: str,
    password: str,
) -> bool:
    user = user(async_session, username)
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user
"""
