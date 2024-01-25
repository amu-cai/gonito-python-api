
from fastapi import APIRouter, UploadFile, File, Depends
import json
from data.models import Challenge, ChallengeReadme
from data.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from pathlib import Path
import challenges.challenges_helper as challenges_helper

router = APIRouter(
    prefix="/challenges",
    tags=['challenges']
)

f = open('configure.json')
data = json.load(f)
STORE = data['store_path']

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
challenges_dir = f"{STORE}/challenges"

class ChallengeInputModel(BaseModel):
    title: str
    description: str | None = None
    type: str
    main_metric: str
    deadline: str | None = None
    award: str | None = None

@router.post("/create-challenge")
async def create_challenge(db: db_dependency, challenge_input_model: ChallengeInputModel):
    challenges_helper.check_challenge_title(challenge_input_model.title)
    challenges_helper.check_challenge_already_in_db(db, challenge_input_model.title)
    Path(f"{STORE}/temp/created_challenge_title").mkdir(parents=True, exist_ok=True)
    temp_challenge_title = f"{STORE}/temp/created_challenge_title/{challenge_input_model.title}"
    with open(temp_challenge_title, "a") as f:
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

@router.post("/create-challenge-details")
async def create_challenge_details(db: db_dependency, challenge_file:UploadFile = File(...)):
    challenge_title = challenges_helper.load_challenge_title_from_temp()
    challenges_helper.check_file_extension(challenge_file)
    temp_zip_path = await challenges_helper.save_zip_file(challenge_file)
    challenge_folder_name = await challenges_helper.extract_challenge(db, challenge_title, temp_zip_path, challenges_dir)
    readme = open(f"{challenges_dir}/{challenge_folder_name}/README.md", "r")
    readme_content = readme.read()
    create_challenge_readme_model = ChallengeReadme(
        challenge_title = challenge_folder_name,
        readme = readme_content,
    )
    db.add(create_challenge_readme_model)
    db.commit()
    return {"success": True, "challenge": challenge_folder_name, "message": "Challenge uploaded successfully"}

@router.get("/get-challenges")
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

@router.get("/{challenge}/readme")
async def get_challenge_readme(db: db_dependency, challenge: str):
    result = [x.readme for x in db.query(ChallengeReadme).where(ChallengeReadme.challenge_title == challenge)][0]
    return result


# TODO: Tylko admin może tworzyć challenge
# TODO: Poprawić kody błędów
# TODO: Readme wsadzić do bazy i wykorzystać w challenge/readme
# TODO: Stworzenie challenge'a poprzez adres url githuba ??? (i tak musi być niewidoczne test-A/expected.tsv)