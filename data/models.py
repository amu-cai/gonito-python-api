from data.database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean)

class Challenge(Base):
    __tablename__ = 'challenges'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    type = Column(String)
    describe = Column(String)
    main_metric = Column(String)
    best_score = Column(String)
    deadline = Column(String)
    prize = Column(String)