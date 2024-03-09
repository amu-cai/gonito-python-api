from database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, UnicodeText, ForeignKey, Float

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean)
    is_author = Column(Boolean)

class Challenge(Base):
    __tablename__ = 'challenges'

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String, ForeignKey("users.username"))
    title = Column(String, ForeignKey("challenges.title"))
    source = Column(String)
    type = Column(String)
    description = Column(String)
    main_metric = Column(String)
    main_metric_parameters = Column(String)
    best_score = Column(Float)
    deadline = Column(String)
    award = Column(String)
    readme = Column(UnicodeText)
    deleted = Column(Boolean)

class Submission(Base):
    __tablename__ = 'submission'

    id = Column(Integer, primary_key=True, index=True)
    challenge = Column(String, ForeignKey("challenges.title"))
    submitter = Column(String, ForeignKey("users.username"))
    description = Column(String)
    dev_result = Column(Float)
    test_result = Column(Float)
    timestamp = Column(String)
    deleted = Column(Boolean)
