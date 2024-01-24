import zipfile
import os
from glob import glob
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Form
from secrets import token_hex
import json
from data.models import Challenge, ChallengeReadme
from data.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel

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

def check_challenge_already_exist(db, challenge_title):
    current_challenges_db = [challenge.title for challenge in db.query(Challenge).all()]
    if challenge_title in current_challenges_db:
        raise HTTPException(status_code=401, detail='Challenge has been already created!')

def check_challenge_title(challenge_title):
    if challenge_title == "":
        raise HTTPException(status_code=401, detail='Invalid challenge title')

def delete_challenge_by_title(db, challenge_title):
    challenges_db = [[challenge.id, challenge.title] for challenge in db.query(Challenge).all()]
    challenge_id = [challenge[0] for challenge in challenges_db if challenge[1] == challenge_title][0]
    challenge = db.get(Challenge, challenge_id)
    db.delete(challenge)
    db.commit()

def check_challenge_already_exist(challenge_folder_name):
    current_challenges = [x.replace(f"{challenges_dir}\\", '') for x in glob(f"{challenges_dir}/*")]
    if challenge_folder_name in current_challenges:
        return True

def check_file_extension(file):
    file_ext = file.filename.split(".").pop()
    if file_ext != "zip":
        raise HTTPException(status_code=401, detail='Bad extension')

def check_challenge_structure(zip_ref, challenge_name):
    challenge_files = [file_obj.filename for file_obj in zip_ref.filelist]
    required_files = ["README.md", "dev-0/expected.tsv", "test-A/expected.tsv"]
    for file in required_files:
        if not f"{challenge_name}/{file}" in challenge_files:
            return True

async def save_zip_file(challenge_file):
    file_name = token_hex(10)
    file_path = f"{file_name}.zip"
    temp_zip_path = f"{STORE}/temp/{file_path}"
    with open(temp_zip_path, "wb") as f:
        content = await challenge_file.read()
        f.write(content)
    return temp_zip_path

def check_challenge_folder_name(challenge_title, challenge_name):
    return not challenge_title == challenge_name

async def extract_challenge(db, challenge_title, temp_zip_path, challenges_dir):
    with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
        challenge_name = zip_ref.filelist[0].filename[:-1]
        folder_name_error = check_challenge_folder_name(challenge_title, challenge_name)
        challenge_already_exist_error = check_challenge_already_exist(challenge_name)
        structure_error = check_challenge_structure(zip_ref, challenge_name)
        zip_ref.extractall(challenges_dir)
    os.remove(temp_zip_path)
    if folder_name_error:
        delete_challenge_by_title(challenge_title)
        raise HTTPException(status_code=401, detail='Invalid challenge folder name - is not equal to challenge title')
    if challenge_already_exist_error:
        delete_challenge_by_title(challenge_title)
        raise HTTPException(status_code=401, detail='Challenge already exist in store!')
    if structure_error:
        delete_challenge_by_title(challenge_title)
        required_files = ["README.md", "dev-0/expected.tsv", "test-A/expected.tsv"]
        raise HTTPException(status_code=401, detail=f'Bad challenge structure! Challenge required files: {str(required_files)}')
    return challenge_name

def load_challenge_title_from_temp():
    challenge_title_path = [x.replace("\\", '') for x in glob(f"{STORE}/temp/created_challenge_title/*")]
    challenge_title = challenge_title_path[0]
    os.remove(f"challenge_title_path/{challenge_title}")
    return challenge_title

@router.post("/create-challenge")
async def create_challenge(db: db_dependency, challenge_input_model: ChallengeInputModel):
    check_challenge_title(challenge_input_model.title)
    check_challenge_already_exist(db, challenge_input_model.title)
    temp_challenge_title = f"{STORE}/temp/created_challenge_title/{challenge_input_model.title}"
    with open(temp_challenge_title, "wb") as f:
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
    return challenge_input_model

@router.post("/create-challenge-details")
async def create_challenge_details(db: db_dependency, challenge_file:UploadFile = File(...)):
    challenge_title = load_challenge_title_from_temp()
    check_file_extension(challenge_file)
    temp_zip_path = await save_zip_file(challenge_file)
    challenge_folder_name = await extract_challenge(db, challenge_title, temp_zip_path, challenges_dir)
    readme = open(f"{challenges_dir}/{challenge_folder_name}/README.md", "r")
    readme_content = readme.read()
    create_challenge_readme_model = ChallengeReadme(
        challenge_title = challenge_folder_name,
        readme = readme_content,
    )
    db.add(create_challenge_readme_model)
    db.commit()
    # TODO: Tylko admin może tworzyć challenge
    # TODO: Poprawić kody błędów
    # TODO: Readme wsadzić do bazy i wykorzystać w challenge/readme
    # TODO: Stworzenie challenge'a poprzez adres url githuba ??? (i tak musi być niewidoczne test-A/expected.tsv)
    return {"success": True, "challenge": challenge_name, "message": "Challenge uploaded successfully"}

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
