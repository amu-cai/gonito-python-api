from sqlalchemy import (
    select,
)
from database_sqlite.models import User
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)
from admin.models import UserRightsModel

async def get_users_settings(async_session):
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

async def user_rights_update(async_session: async_sessionmaker[AsyncSession], user_rights: UserRightsModel):
    is_admin = user_rights.is_admin
    is_author = user_rights.is_author
    user_to_update = user_rights.username
    async with async_session as session:
        user = (await session.execute(select(User).filter_by(username=user_to_update))).scalars().one()
        user.is_admin = is_admin
        user.is_author = is_author
        await session.commit()
    return {"success": True, "user": user_to_update, "message": "User rights uploaded successfully"}