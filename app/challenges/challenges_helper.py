import zipfile
import os
import json
from global_helper import check_challenge_in_store, check_zip_structure
from fastapi import HTTPException
from database_sqlite.models import Challenge
from shutil import rmtree
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)
from os.path import exists

f = open('configure.json')
data = json.load(f)
STORE = data['store_path']
challenges_dir = f"{STORE}/challenges"

def check_challenge_title(challenge_title):
    if challenge_title == "":
        raise HTTPException(status_code=422, detail=f'{challenge_title}: Invalid challenge title')

async def delete_challenge_by_title(async_session, challenge_title):
    async with async_session as session:
        challenge_id = [challenge.id for challenge in session.query(Challenge).where(Challenge.title == challenge_title)][0]
        challenge = session.get(Challenge, challenge_id)
        session.delete(challenge)
        await session.commit()

def check_file_extension(async_session: async_sessionmaker[AsyncSession], file, challenge_title):
    file_ext = file.filename.split(".").pop()
    if file_ext != "zip":
        delete_challenge_by_title(async_session, challenge_title)
        raise HTTPException(status_code=422, detail='Bad extension')

async def extract_challenge(async_session: async_sessionmaker[AsyncSession], challenge_title, temp_zip_path, challenges_dir):
    required_challenge_files = ["README.md", "dev-0/expected.tsv", "test-A/expected.tsv"]

    with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
        challenge_name = zip_ref.filelist[0].filename[:-1]

        folder_name_error = not challenge_title == challenge_name
        challenge_already_exist_error = check_challenge_in_store(challenge_name)
        structure_error = check_zip_structure(zip_ref, challenge_name, required_challenge_files)

        if True not in [folder_name_error, challenge_already_exist_error, structure_error]:
            for file in required_challenge_files:
                zip_ref.extract(f"{challenge_name}/{file}", challenges_dir)

    os.remove(temp_zip_path)

    if folder_name_error:
        if exists(f"{challenges_dir}/{challenge_name}"):
            rmtree(f"{challenges_dir}/{challenge_name}")
        delete_challenge_by_title(async_session, challenge_title)
        raise HTTPException(status_code=422, detail=f'Invalid challenge folder name "{challenge_name}" - is not equal to challenge title "{challenge_title}"')

    if challenge_already_exist_error:
        if exists(f"{challenges_dir}/{challenge_name}"):
            rmtree(f"{challenges_dir}/{challenge_name}")
        delete_challenge_by_title(async_session, challenge_title)
        raise HTTPException(status_code=422, detail=f'Challenge "{challenge_name}" already exist in store!')

    if structure_error:
        if exists(f"{challenges_dir}/{challenge_name}"):
            rmtree(f"{challenges_dir}/{challenge_name}")
        delete_challenge_by_title(async_session, challenge_title)
        raise HTTPException(status_code=422, detail=f'Bad challenge structure! Challenge required files: {str(required_challenge_files)}')

    return challenge_name