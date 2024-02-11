import json

from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from database_handler.db_connection import get_engine, get_session
from database_handler.base_table import Base
from database_handler.challenges import (
    ChallengeInput,
    challenge_exists,
    create_challenge,
    all_challenges,
    update_challenge_best_score,
)
from database_handler.users import (
    UserInput,
    user_exists,
    create_user,
    user,
)

import evaluation.evaluation_helper as evaluation_helper

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = get_engine()
session = get_session(engine)


############################################################################
# TODO AUTH
f = open('configure.json')
data = json.load(f)
SECRET_KEY = data['key']
ALGORITHM = data['algorithm']

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


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
#########################################################################


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = session()
    try:
        yield db
    finally:
        await db.close()

db_dependency = Annotated[AsyncSession, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


###############################################################################
# challenges

# TODO: Only admin can create challenge
@app.post("/create-challenge", status_code=201)
async def post_create_challenge(db: db_dependency, input: ChallengeInput):
    if not await challenge_exists(db, input.title):
        await create_challenge(db, input)
    else:
        message = f"Challenge {input.title} already exists"
        raise HTTPException(status_code=422, detail=message)


@app.get("/all-challenges", status_code=200)
async def get_all_challenges(db: db_dependency):
    raw_challenges = await all_challenges(db)
    dict_challenges = [x.to_dict() for x in raw_challenges]

    return dict_challenges


@app.post("/change-challenge-best-score", status_code=200)
async def post_change_challenge_best_score(
    db: db_dependency,
    title: str,
    new_best_score: str,
):
    if await challenge_exists(db, title):
        await update_challenge_best_score(db, title, new_best_score)
    else:
        message = f"Challenge {title} does not exist"
        raise HTTPException(status_code=422, detail=message)


###############################################################################
# users

@app.post("/create-user", status_code=201)
async def post_create_user(db: db_dependency, input: UserInput):
    if not await user_exists(db, input.username):
        await create_user(db, input)
    else:
        message = f"User {input.username} already exists"
        raise HTTPException(status_code=422, detail=message)


@app.get("/user")
async def get_user(db: db_dependency, username: str):
    user_data = await user(db, username)

    if user_data:
        return user_data.to_dict()
    else:
        message = f"User {username} does not exist"
        raise HTTPException(status_code=404, detail=message)


###############################################################################
# submissions

@app.post("/submit")
async def submit(db: db_dependency, submission_file: UploadFile = File(...)):
    result = []
    evaluation_helper.check_file_extension(submission_file)
    temp_zip_path = await evaluation_helper.save_zip_file(submission_file)
    challenge_folder_name = await evaluation_helper.extract_submission(temp_zip_path)
    return result


###############################################################################
# metrics

# TODO
@app.get("/get-metrics")
async def get_metrics(db: db_dependency):
    result = [{"name": "Accuracy"}, {"name": "F1"}]
    return result


###############################################################################
# AUTH
class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}
# AUTH
###############################################################################
# TODOS
# - Readme wsadzić do bazy i wykorzystać w challenge/readme
# - Stworzenie challenge'a poprzez adres url githuba ??? (i tak musi być niewidoczne test-A/expected.tsv)
