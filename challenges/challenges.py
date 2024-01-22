import zipfile
import os
from glob import glob
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Form
from secrets import token_hex
import json
import shutil
from data.models import Challenge
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

class ChallengeInputModel(BaseModel):
    title: str
    description: str | None = None
    type: str
    main_metric: str
    deadline: str | None = None
    award: str | None = None

@router.post("/create-challenge")
async def create_challenge(db: db_dependency, challenge_input_model: ChallengeInputModel):
    current_challenges_db = [challenge.title for challenge in db.query(Challenge).all()]
    if challenge_input_model.title in current_challenges_db:
        raise HTTPException(status_code=401, detail='Challenge has been already created!')
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

def check_file_extension(file):
    file_ext = file.filename.split(".").pop()
    if file_ext != "zip":
        raise HTTPException(status_code=401, detail='Bad extension')

@router.post("/create-challenge-details")
async def create_challenge_details(db: db_dependency, challenge_file:UploadFile = File(...)):
    check_file_extension(challenge_file)

    challenges_dir = f"{STORE}/challenges"
    file_name = token_hex(10)
    file_path = f"{file_name}.zip"
    
    with open(f"{STORE}/temp/{file_path}", "wb") as f:
        content = await challenge_file.read()
        f.write(content)

    challenge_name = ""

    already_exist_error = False
    with zipfile.ZipFile(f"{STORE}/temp/{file_path}", 'r') as zip_ref:
        current_challenges = [x.replace(f"{challenges_dir}\\", '') for x in glob(f"{challenges_dir}/*")]
        challenge_name = zip_ref.filelist[0].filename[:-1]
        current_challenges_db = [challenge.title for challenge in db.query(Challenge).all()]
        if (challenge_name in current_challenges) or (challenge_name in current_challenges_db):
            already_exist_error = True
        zip_ref.extractall(challenges_dir)

    os.remove(f"{STORE}/temp/{file_path}")

    if already_exist_error:
        raise HTTPException(status_code=401, detail='Challenge has been already created!')

    dev_dir = glob(f"{challenges_dir}/{challenge_name}/dev-0/*")
    dev_dir_files = [x.split('\\')[1] for x in dev_dir]
    challenge__dir_files = glob(f"{challenges_dir}/{challenge_name}/*")
    challenge_files = [x.split('\\')[1] for x in challenge__dir_files]

    if (not "expected.tsv" in dev_dir_files) or (not "README.md" in challenge_files):
        # TODO: Sprawdzić więcej rzeczy jeśli będzie potrzebne
        shutil.rmtree(f"{challenges_dir}/{challenge_name}")
        raise HTTPException(status_code=401, detail='Bad challenge structure!')

    challenge_model = {
        "name": "",
        "type": "",
        "main_metric": "",
        "best_score": "",
        "deadline": "",
        "description": "",
        "award": ""
    }

    # with open(f"{challenges_dir}/{challenge_name}/README.md", "r") as file:
    #     readme_lines = file.readlines()
    #     for line in readme_lines:
    #         if ":" in line:
    #             attribute = line.split(':')[0].replace(" ", "", 1)
    #             value = line.split(':')[1].replace(" ", "", 1)[:-1]
    #             if attribute in challenge_model.keys():
    #                 challenge_model[attribute] = value

    if challenge_model["title"] == "":
        shutil.rmtree(f"{challenges_dir}/{challenge_name}")
        raise HTTPException(status_code=401, detail='Challenge title not finded!')

    # TODO: W tym miejscu zrobić update lub połączyć requesty, albo ten request będzie tworzył nowy endpoint, taki który dotyczy szczegółów challenge'a      
    create_challenge_model = Challenge(
        title = challenge_model["title"],
        type = challenge_model["type"],
        describe = challenge_model["describe"],
        main_metric = challenge_model["main_metric"],
        best_score = challenge_model["best_score"],
        deadline = challenge_model["deadline"],
        award = challenge_model["award"],
    )
    db.add(create_challenge_model)
    db.commit()
    
    # TODO: Brać tylko potrzebne pliki z challeng'u, reszte usuwać
    # TODO: Tylko admin może tworzyć challenge
    # TODO: Poprawić kody błędów
    # TODO: Stworzenie challenge'a poprzez adres url githuba
    # TODO: Readme wsadzić do bazy i wykorzystać w challenge/readme

    return {"success": True, "file_path": file_path, "message": "File uploaded successfully"}


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
