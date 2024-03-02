from sqlalchemy import (
    select,
)
from database_sqlite.models import User

async def get_user_settings(async_session):
    async with async_session as session:
        users = (await session.execute(select(User))).scalars().all()
    result = []
    for user in users:
        result.append({
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
            "is_author": user.is_author,
        })
    return result