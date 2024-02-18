from datetime import timedelta, datetime
from typing import Annotated
from fastapi import Depends, HTTPException
from starlette import status
from database_sqlite.models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from auth.models import CreateUserRequest
import json
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy import (
    select,
)

f = open('configure.json')
data = json.load(f)
SECRET_KEY = data['key']
ALGORITHM = data['algorithm']

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

async def authenticate_user(username: str, password: str, async_session: AsyncSession):
    async with async_session as session:
        user = await session.execute(select(Users)).filter_by(title=username).scalars().one()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

async def create_user(async_session, create_user_request: CreateUserRequest):
    async with async_session as session:
        users_exist = len(await session.execute(select(Users)).scalars().one()) > 0

    is_admin = False
    if not users_exist:
        is_admin = True
        
    create_user_model = Users(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_admin=is_admin
    )

    async with async_session as session:
        async_session.add(create_user_model)
        await session.commit()

    return {'message': "challege created!"}

async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], async_session):
    user = authenticate_user(form_data.username, form_data.password, async_session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}