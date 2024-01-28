from database_handler.base_table import Base

from sqlalchemy.sql import text
from sqlalchemy import (
    Column,
    Integer,
    String,
    select,
)
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    type = Column(String)
    description = Column(String)
    main_metric = Column(String)
    best_score = Column(String)
    deadline = Column(String)
    award = Column(String)


async def insert_challenge(
    async_session: async_sessionmaker[AsyncSession],
    challenge: Challenge,
) -> None:
    async with async_session() as session:
        session.add_all([challenge])
        await session.commit()


async def get_all_challenges(
    async_session: async_sessionmaker[AsyncSession]
) -> None:
    async with async_session() as session:
        result = await session.execute(select(Challenge.id))

    return result.fetchall()


async def update_challenge_best_score(
    async_session: async_sessionmaker[AsyncSession],
    id: int,
    new_best_score: str,
) -> None:
    async with async_session() as session:
        await session.execute(text(
            """UPDATE challenges
                  SET best_score = 'aaaaaaaaa'
                WHERE id = 1"""
        ))
        await session.commit()
