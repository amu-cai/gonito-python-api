import zipfile
import os
from glob import glob
from fastapi import APIRouter, HTTPException, UploadFile, File
from secrets import token_hex
import json
import shutil

router = APIRouter(
    prefix="/challenges",
    tags=['challenges']
)

f = open('configure.json')
data = json.load(f)
STORE = data['store_path']

@router.post("/create-challenge")
async def create_challenge(file:UploadFile = File(...)):
    file_ext = file.filename.split(".").pop()
    if file_ext != "zip":
        raise HTTPException(status_code=401, detail='Bad extension')

    challenges_dir = f"{STORE}/challenges"
    file_name = token_hex(10)
    file_path = f"{file_name}.{file_ext}"
    
    with open(f"{STORE}/temp/{file_path}", "wb") as f:
        content = await file.read()
        f.write(content)

    challenge_name = ""
    already_exist_error = False
    with zipfile.ZipFile(f"{STORE}/temp/{file_path}", 'r') as zip_ref:
        current_challenges = [x.replace(f"{challenges_dir}\\", '') for x in glob(f"{challenges_dir}/*")]
        challenge_name = zip_ref.filelist[0].filename[:-1]
        if challenge_name in current_challenges:
            already_exist_error = True
        zip_ref.extractall(challenges_dir)

    os.remove(f"{STORE}/temp/{file_path}")

    dev_dir = glob(f"{challenges_dir}/{challenge_name}/dev-0/*")
    dev_dir_files = [x.split('\\')[1] for x in dev_dir]
    challenge__dir_files = glob(f"{challenges_dir}/{challenge_name}/*")
    challenge_files = [x.split('\\')[1] for x in challenge__dir_files]
    
    if (not "expected.tsv" in dev_dir_files) or (not "README.md" in challenge_files):
        # TODO: Sprawdzić więcej rzeczy jeśli będzie potrzebne
        shutil.rmtree(f"{challenges_dir}/{challenge_name}")
        raise HTTPException(status_code=401, detail='Bad challenge structure!')

    if already_exist_error:
        raise HTTPException(status_code=401, detail='Challenge has been already created!')
    
    # TODO: Brać tylko potrzebne pliki z challeng'u, reszte usuwać
    # TODO: Tylko admin może tworzyć challenge
    # TODO: Poprawić kody błędów
    # TODO: Stworzenie challenge'a poprzez adres url githuba

    return {"success": True, "file_path": file_path, "message": "File uloaded successfully"}