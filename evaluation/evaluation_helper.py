import zipfile
import os
from glob import glob
from fastapi import HTTPException
from data.models import Submission
from secrets import token_hex
import json

f = open('configure.json')
data = json.load(f)
STORE = data['store_path']
challenges_dir = f"{STORE}/challenges"

def check_file_extension(file):
    file_ext = file.filename.split(".").pop()
    if file_ext != "zip":
        raise HTTPException(status_code=401, detail='Bad extension')

async def save_zip_file(file):
    file_name = token_hex(10)
    file_path = f"{file_name}.zip"
    temp_zip_path = f"{STORE}/temp/{file_path}"
    with open(temp_zip_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return temp_zip_path

async def extract_submission(temp_zip_path):
    required_files = ["dev-0/out.tsv", "test-A/out.tsv"]
    with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
        challenge_name = zip_ref.filelist[0].filename[:-1]
        submission_dir = f"{challenges_dir}/{challenge_name}/submissions"
        for file in required_files:
            zip_ref.extract(f"{challenge_name}/{file}", submission_dir)
    os.remove(temp_zip_path)