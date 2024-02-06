from database_handler.base_table import Base

from pydantic import BaseModel
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
    readme = Column(String)


class ChallengeInput(BaseModel):
    title: str
    type: str
    description: str | None
    main_metric: str
    best_score: str
    deadline: str | None
    award: str | None
    readme: str | None


async def insert_challenge(
    async_session: async_sessionmaker[AsyncSession],
    input: ChallengeInput,
) -> None:
    async with async_session as session:
        challenge_to_insert = Challenge(
            title=input.title,
            type=input.type,
            description=input.description,
            main_metric=input.main_metric,
            best_score=input.best_score,
            deadline=input.deadline,
            award=input.award,
            readme=input.readme,
        )
        session.add_all([challenge_to_insert])
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
