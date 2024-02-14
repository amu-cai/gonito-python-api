from fastapi import UploadFile, File
from database_sqlite.models import Challenge, ChallengeInfo
from pathlib import Path
import challenges.challenges_helper as challenges_helper
from challenges.models import ChallengeInputModel
import json

f = open('configure.json')
data = json.load(f)
STORE = data['store_path']

challenges_dir = f"{STORE}/challenges"

async def create_challenge(db, challenge_input_model: ChallengeInputModel):
    challenges_helper.check_challenge_title(challenge_input_model.title)
    challenges_helper.check_challenge_already_in_db(db, challenge_input_model.title)
    challenge_temp_path = f"{STORE}/temp/challenge_created"
    Path(challenge_temp_path).mkdir(parents=True, exist_ok=True)
    temp_challenge_created = f"{challenge_temp_path}/{challenge_input_model.title}"
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

async def create_challenge_details(db, challenge_file:UploadFile = File(...)):
    challenge = challenges_helper.load_challenge_from_temp(db)
    challenges_helper.check_file_extension(db, challenge_file, challenge.title)
    temp_zip_path = await challenges_helper.save_zip_file(challenge_file)
    challenge_folder_name = await challenges_helper.extract_challenge(db, challenge.title, temp_zip_path, challenges_dir)
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

async def get_challenges(db):
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

async def get_challenge_readme(db, challenge: str):
    challenge_info = [x for x in db.query(ChallengeInfo).where(ChallengeInfo.title == challenge)][0]
    return {
        "id": challenge_info.id, 
        "title": challenge_info.title,
        "description": challenge_info.description,
        "readme": challenge_info.readme
    }


# TODO: Tylko admin może tworzyć challenge
# TODO: Poprawić kody błędów
# TODO: Readme wsadzić do bazy i wykorzystać w challenge/readme
# TODO: Stworzenie challenge'a poprzez adres url githuba ??? (i tak musi być niewidoczne test-A/expected.tsv)