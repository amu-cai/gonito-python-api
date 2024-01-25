from data.database import Base
from sqlalchemy import Column, Integer, String, Boolean, UnicodeText, ForeignKey

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean)

class Metric(Base):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class Challenge(Base):
    __tablename__ = 'challenges'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    type = Column(String)
    description = Column(String)
    main_metric = Column(String)
    best_score = Column(String)
    deadline = Column(String)
    award = Column(String)

class ChallengeReadme(Base):
    __tablename__ = 'challenges_readme'

    id = Column(Integer, primary_key=True, index=True)
    challenge_title = Column(String, ForeignKey("challenges.title"))
    readme = Column(UnicodeText)

