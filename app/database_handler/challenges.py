from database_handler.base_table import Base

from pydantic import BaseModel
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

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ChallengeInput(BaseModel):
    title: str
    type: str
    description: str | None
    main_metric: str
    best_score: str
    deadline: str | None
    award: str | None
    readme: str | None


async def challenge_exists(
    async_session: async_sessionmaker[AsyncSession],
    title: str,
) -> bool:
    async with async_session as session:
        challenge_exists = (
            await session.execute(
                select(Challenge.title).filter_by(title=title)
            )
        ).fetchone() is not None

    return challenge_exists


async def create_challenge(
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


async def all_challenges(
    async_session: async_sessionmaker[AsyncSession]
) -> list[Challenge]:
    async with async_session as session:
        challenges = await session.execute(select(Challenge))

    return challenges.scalars().all()


async def update_challenge_best_score(
    async_session: async_sessionmaker[AsyncSession],
    title: str,
    new_best_score: str,
) -> None:
    async with async_session as session:
        challenge_to_update = (
            await session.execute(
                select(Challenge).filter_by(title=title)
            )
        ).scalars().one()

        challenge_to_update.best_score = new_best_score
        await session.commit()
