from database_sqlite.models import Submission
import evaluation.evaluation_helper as evaluation_helper
from datetime import datetime
from fastapi import UploadFile, File, Form, HTTPException
import zipfile
from global_helper import check_challenge_in_store, check_zip_structure, save_zip_file, check_challenge_exists
import os

async def submit(async_session, description, challenge_title, submitter, submission_file:UploadFile = File(...)):
    challenge_exists = await check_challenge_exists(async_session, challenge_title)
    if not challenge_exists:
        raise HTTPException(status_code=422, detail=f'{challenge_title} challenge not exist!')

    submitter = evaluation_helper.check_submitter(submitter)
    description = evaluation_helper.check_description(description)

    temp_zip_path = await save_zip_file(submission_file)

    dev_result = 0
    test_result = 0

    required_submission_files = ["dev-0/out.tsv", "test-A/out.tsv"]
    with zipfile.ZipFile(submission_file, 'r') as zip_ref:
        challenge_name = zip_ref.filelist[0].filename[:-1]

        folder_name_error = not challenge_title == challenge_name
        challenge_not_exist_error = not check_challenge_in_store(challenge_name)
        structure_error = check_zip_structure(zip_ref, challenge_name, required_submission_files)

        if True not in [folder_name_error, challenge_not_exist_error, structure_error]:
            for file in zip_ref.filelist:
                if file.filename == f"{challenge_name}/dev-0/out.tsv":
                    with zip_ref.open(file, "r") as file_content:
                        # TODO: evaluation
                        dev_result = file_content.split('\n')[0]
                if file.filename == f"{challenge_name}/test-A/out.tsv":
                    with zip_ref.open(file, "r") as file_content:
                        # TODO: evaluation
                        test_result = file_content.split('\n')[0]
                    
    os.remove(temp_zip_path)

    if folder_name_error:
        raise HTTPException(status_code=422, detail=f'Invalid challenge folder name "{challenge_name}" - is not equal to challenge title "{challenge_title}"')

    if challenge_not_exist_error:
        raise HTTPException(status_code=422, detail=f'Challenge "{challenge_name}" not exist in store!')

    if structure_error:
        raise HTTPException(status_code=422, detail=f'Bad challenge structure! Challenge required files: {str(required_submission_files)}')

    when = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    create_submission_model = Submission(
        challenge = challenge_title,
        submitter = submitter,
        description = description,
        dev_result = dev_result,
        test_result = test_result,
        when = when,
    )
    async_session.add(create_submission_model)
    async_session.commit()
    return {"success": True, "submission": "description", "message": "Submission added successfully"}

async def get_metrics():
    result =  [{"name": "Accuracy"}, {"name": "Precision"}]
    return result

async def get_all_submissions(db, challenge: str):
    result = []
    submissions = db.query(Submission).where(Submission.challenge == challenge)
    for submission in submissions:
        result.append({
            "id": submission.id,
            "submitter": submission.submitter,
            "description": submission.description,
            "dev_result": submission.dev_result,
            "test_result": submission.test_result,
            "when": submission.when,
        })
    return result