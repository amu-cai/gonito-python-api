import zipfile
import os
from glob import glob
from fastapi import APIRouter, HTTPException, UploadFile, File
from secrets import token_hex
import json

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
    already_exist_error = False
    with zipfile.ZipFile(f"{STORE}/temp/{file_path}", 'r') as zip_ref:
        current_challenges = [x.replace(f"{challenges_dir}\\", '') for x in glob(f"{challenges_dir}/*")]
        if zip_ref.filelist[0].filename[:-1] in current_challenges:
            already_exist_error = True
        zip_ref.extractall(challenges_dir)
    os.remove(f"{STORE}/temp/{file_path}")
    if already_exist_error:
        raise HTTPException(status_code=401, detail='Challenge has been already created!')
    # TODO: Sprawdzanie struktury challenge'a, tylko admin może tworzyć challenge, refactor, inny kod błędu na istniejący już challenge
    return {"success": True, "file_path": file_path, "message": "File uloaded successfully"}