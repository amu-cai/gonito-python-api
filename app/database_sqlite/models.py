from database_sqlite.database_sqlite import Base
from sqlalchemy import Column, Integer, String, Boolean, UnicodeText, ForeignKey, Float

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean)
    is_author = Column(Boolean)

class Metric(Base):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class Challenge(Base):
    __tablename__ = 'challenges'

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String)
    title = Column(String, unique=True)
    source = Column(String)
    type = Column(String)
    description = Column(String)
    main_metric = Column(String)
    best_score = Column(Float)
    deadline = Column(String)
    award = Column(String)
    readme = Column(UnicodeText)

class ChallengeInfo(Base):
    __tablename__ = 'challenge_info'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, ForeignKey("challenges.title"))
    description = Column(String)
    readme = Column(UnicodeText)

class Submission(Base):
    __tablename__ = 'submission'

    id = Column(Integer, primary_key=True, index=True)
    challenge = Column(String, ForeignKey("challenges.title"))
    submitter = Column(String, unique=True)
    description = Column(String)
    dev_result = Column(Float)
    test_result = Column(Float)
    timestamp = Column(String)
