from typing import Annotated
from fastapi import Depends, FastAPI, status, HTTPException
# import auth.auth
# import challenges.challenges_helper as challenges_helper
# import challenges.challenges
# from auth.auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from datetime import timedelta, datetime
from pydantic import BaseModel
# from data.models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import json

from sqlalchemy.ext.asyncio import AsyncSession

from database_handler.challenges import ChallengeInput
from database_handler.db_connection import get_engine, get_session
from database_handler.base_table import Base
from database_handler.challenges import (
    Challenge,
    insert_challenge,
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


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return {"User": user}


@app.post("/insert_challenge")
async def post_insert_challenge(db: db_dependency, input: ChallengeInput):
    await insert_challenge(db, input)


@app.post("/submit")
async def submit(db: db_dependency, submission_file: UploadFile = File(...)):
    result = []
    evaluation_helper.check_file_extension(submission_file)
    temp_zip_path = await evaluation_helper.save_zip_file(submission_file)
    challenge_folder_name = await evaluation_helper.extract_submission(temp_zip_path)
    return result


@app.get("/get-metrics")
async def get_metrics(db: db_dependency):
    result = [{"name": "Accuracy"}, {"name": "F1"}]
    return result


###############################################################################
# AUTH
class CreateUserRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
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


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    users_exist = len(db.query(Users).offset(0).limit(1).all()) > 0
    is_admin = False
    if not users_exist:
        is_admin = True
    create_user_model = Users(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_admin=is_admin
    )
    db.add(create_user_model)
    db.commit()


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
###############################################################################
# CHALLENGES


"""
class ChallengeInputModel(BaseModel):
    title: str
    description: str | None = None
    type: str
    main_metric: str
    deadline: str | None = None
    award: str | None = None


@app.post("/create-challenge")
async def create_challenge(db: db_dependency, challenge_input_model: ChallengeInputModel):
    challenges_helper.check_challenge_title(challenge_input_model.title)
    challenges_helper.check_challenge_already_in_db(db, challenge_input_model.title)
    challenge_temp_path = f"{STORE}/temp/challenge_created"
    Path(challenge_temp_path).mkdir(parents=True, exist_ok=True)
    temp_challenge_created = f"{challenge_temp_path}/{challenge_input_model.title}"
    print(temp_challenge_created)
    with open(temp_challenge_created, "a") as f:
        f.write(challenge_input_model.title)
    best_score = "0"
    create_challenge_model = Challenge(
        title = challenge_input_model.title,
        type = challenge_input_model.type,
        description = challenge_input_model.description,
        main_metric = challenge_input_model.main_metric,
        best_score = best_score,
        deadline = challenge_input_model.deadline,
        award = challenge_input_model.award,
    )
    db.add(create_challenge_model)
    db.commit()
    return {"success": True, "challenge": challenge_input_model.title, "message": "Challenge data added successfully"}


@app.post("/create-challenge-details")
async def create_challenge_details(db: db_dependency, challenge_file:UploadFile = File(...)):
    challenge = challenges_helper.load_challenge_from_temp(db)
    challenges_helper.check_file_extension(challenge_file)
    temp_zip_path = await challenges_helper.save_zip_file(challenge_file)
    challenge_folder_name = await challenges_helper.extract_challenge(challenge.title, temp_zip_path, challenges_dir)
    readme = open(f"{challenges_dir}/{challenge_folder_name}/README.md", "r")
    readme_content = readme.read()
    create_challenge_readme_model = ChallengeInfo(
        title = challenge.title,
        description = challenge.description,
        readme = readme_content,
    )
    db.add(create_challenge_readme_model)
    db.commit()
    return {"success": True, "challenge": challenge_folder_name, "message": "Challenge uploaded successfully"}


@app.get("/get-challenges")
async def get_challenges(db: db_dependency):
    result = []
    for challenge in db.query(Challenge).all():
        result.append({
            "id": challenge.id,
            "title": challenge.title,
            "type": challenge.type,
            "description": challenge.description,
            "mainMetric": challenge.main_metric,
            "bestScore": challenge.best_score,
            "deadline": challenge.deadline,
            "award": challenge.award,
        })
    return result


@app.get("/challenge/{challenge}")
async def get_challenge_readme(db: db_dependency, challenge: str):
    challenge_info = [x for x in db.query(ChallengeInfo).where(ChallengeInfo.title == challenge)][0]
    return {
        "id": challenge_info.id, 
        "title": challenge_info.title,
        "description": challenge_info.description,
        "readme": challenge_info.readme
    }
"""


# TODO: Tylko admin może tworzyć challenge
# TODO: Poprawić kody błędów
# TODO: Readme wsadzić do bazy i wykorzystać w challenge/readme
# TODO: Stworzenie challenge'a poprzez adres url githuba ??? (i tak musi być niewidoczne test-A/expected.tsv)
