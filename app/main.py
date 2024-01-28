from typing import Annotated
from fastapi import Depends, FastAPI, status, HTTPException
import auth.auth
import challenges.challenges
import evaluation.evaluation
from auth.auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from database_handler.db_connection import get_engine, get_session
from database_handler.base_table import Base
from database_handler.challenges import (
    Challenge,
    insert_challenge,
)

app = FastAPI()

app.include_router(auth.auth.router)
app.include_router(challenges.challenges.router)
app.include_router(evaluation.evaluation.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = get_engine()


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = get_session(engine)
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[AsyncSession, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return {"User": user}


@app.post("/insert_challenge")
async def post_insert_challenge(db: db_dependency):
    example_challenge = Challenge(
        title="title103",
        type="type1",
        description="description1",
        main_metric="metric1",
        best_score="score1",
        deadline="deadline1",
        award="award1",
    )
    insert_challenge(db, example_challenge)
