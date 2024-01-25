import zipfile
import os
from glob import glob
from fastapi import HTTPException
from data.models import Challenge
from secrets import token_hex
import json

f = open('configure.json')
data = json.load(f)
STORE = data['store_path']
challenges_dir = f"{STORE}/challenges"


def check_challenge_already_in_db(db, challenge_title):
    current_challenges_db = [challenge.title for challenge in db.query(Challenge).all()]
    if challenge_title in current_challenges_db:
        raise HTTPException(status_code=401, detail='Challenge has been already created!')

def check_challenge_title(challenge_title):
    if challenge_title == "":
        raise HTTPException(status_code=401, detail='Invalid challenge title')

def delete_challenge_by_title(db, challenge_title):
    challenge_id = [challenge.id for challenge in db.query(Challenge).where(Challenge.challenge_title == challenge_title)][0]
    challenge = db.get(Challenge, challenge_id)
    db.delete(challenge)
    db.commit()

def check_challenge_already_in_store(challenge_folder_name):
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
    required_files = ["README.md", "dev-0/expected.tsv", "test-A/expected.tsv"]
    with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
        challenge_name = zip_ref.filelist[0].filename[:-1]
        folder_name_error = check_challenge_folder_name(challenge_title, challenge_name)
        challenge_already_exist_error = check_challenge_already_in_store(challenge_name)
        structure_error = check_challenge_structure(zip_ref, challenge_name)
        for file in required_files:
            zip_ref.extract(f"{challenge_name}/{file}", challenges_dir)
    os.remove(temp_zip_path)
    if folder_name_error:
        delete_challenge_by_title(challenge_title)
        raise HTTPException(status_code=401, detail='Invalid challenge folder name - is not equal to challenge title')
    if challenge_already_exist_error:
        delete_challenge_by_title(challenge_title)
        raise HTTPException(status_code=401, detail='Challenge already exist in store!')
    if structure_error:
        delete_challenge_by_title(challenge_title)
        raise HTTPException(status_code=401, detail=f'Bad challenge structure! Challenge required files: {str(required_files)}')
    return challenge_name

def load_challenge_title_from_temp():
    challenge_title_path = [x.replace("\\", '/') for x in glob(f"{STORE}/temp/created_challenge_title/*")][0]
    challenge_title = challenge_title_path.split("/")[-1]
    os.remove(challenge_title_path)
    return challenge_title