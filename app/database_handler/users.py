from database_handler.base_table import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean)
