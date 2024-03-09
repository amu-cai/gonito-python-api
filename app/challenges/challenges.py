from fastapi import UploadFile, File, HTTPException
from database.models import Challenge
import challenges.challenges_helper as challenges_helper
from challenges.models import ChallengeInputModel
import json
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy import (
    select,
)
from global_helper import check_challenge_exists, save_zip_file

f = open('configure.json')
data = json.load(f)
STORE = data['store_path']

challenges_dir = f"{STORE}/challenges"

async def create_challenge(async_session: async_sessionmaker[AsyncSession], user, challenge_input_model: ChallengeInputModel, challenge_file:UploadFile = File(...)):
    challenge_title = challenge_input_model.title
    challenges_helper.check_challenge_title(challenge_title)
    challenge_exists = await check_challenge_exists(async_session, challenge_title)
    if challenge_exists:
        raise HTTPException(status_code=422, detail=f'{challenge_title} challenge has been already created!')

    best_score = 0

    challenges_helper.check_file_extension(async_session, challenge_file, challenge_title)
    temp_zip_path = await save_zip_file(challenge_file)
    challenge_folder_name = await challenges_helper.extract_challenge(async_session, challenge_title, temp_zip_path, challenges_dir)
    readme = open(f"{challenges_dir}/{challenge_folder_name}/README.md", "r")
    readme_content = readme.read()

    create_challenge_model = Challenge(
        author = user["username"],
        title = challenge_title,
        type = challenge_input_model.type,
        source = challenge_input_model.challenge_source,
        description = challenge_input_model.description,
        main_metric = challenge_input_model.main_metric,
        best_score = best_score,
        deadline = challenge_input_model.deadline,
        award = challenge_input_model.award,
        readme = readme_content,
        deleted = False
    )

    async with async_session as session:
        session.add(create_challenge_model)
        await session.commit()

    return {"success": True, "challenge": challenge_folder_name, "message": "Challenge uploaded successfully"}


async def all_challenges(
    async_session: async_sessionmaker[AsyncSession]
) -> list[Challenge]:
    async with async_session as session:
        challenges = await session.execute(select(Challenge))
    result = []
    for challenge in challenges.scalars().all():
        result.append({
            "id": challenge.id,
            "title": challenge.title,
            "type": challenge.type,
            "description": challenge.description,
            "mainMetric": challenge.main_metric,
            "bestScore": challenge.best_score,
            "deadline": challenge.deadline,
            "award": challenge.award,
            "deleted": challenge.deleted
        })
    return result

async def get_challenge_info(async_session, challenge: str):
    async with async_session as session:
        challenge_info = (
                await session.execute(
                    select(Challenge).filter_by(title=challenge)
                )
            ).scalars().one()
    return {
        "id": challenge_info.id, 
        "title": challenge_info.title,
        "author": challenge_info.author,
        "type": challenge_info.type,
        "mainMetric": challenge_info.main_metric,
        "description": challenge_info.description,
        "readme": challenge_info.readme,
        "source": challenge_info.source,
        "bestScore": challenge_info.best_score,
        "deadline": challenge_info.deadline,
        "award": challenge_info.award,
        "deleted": challenge_info.deleted
    }