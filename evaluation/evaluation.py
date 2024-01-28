from fastapi import APIRouter, Depends, UploadFile, File
from data.models import Metric, Submission
from data.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
import evaluation.evaluation_helper as evaluation_helper
from pydantic import BaseModel
import requests
from datetime import datetime

router = APIRouter(
    prefix="/evaluation",
    tags=['evaluation']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# @router.post("/submit")
# async def submit(db: db_dependency, submission_file:UploadFile = File(...)):
#     result = []
#     evaluation_helper.check_file_extension(submission_file)
#     temp_zip_path = await evaluation_helper.save_zip_file(submission_file)
#     challenge_folder_name = await evaluation_helper.extract_submission(temp_zip_path)
#     return result

class SubmitInputModel(BaseModel):
    challenge_title: str
    submitter: str
    description: str
    repo_url: str

@router.post("/submit")
async def submit(db: db_dependency, submit_input_model: SubmitInputModel):
    challenge = submit_input_model.challenge_title
    submitter = submit_input_model.submitter
    repo_url = submit_input_model.repo_url
    description = submit_input_model.description
    evaluation_helper.check_repo_url(repo_url)
    evaluation_helper.check_challenge_title(challenge)
    submitter = evaluation_helper.check_submitter(submitter)
    description = evaluation_helper.check_description(description)
    dev_out = requests.get(repo_url + "/raw/branch/master/dev-0/out.tsv").text
    test_out = requests.get(repo_url + "/raw/branch/master/test-A/out.tsv").text
    dev_result = dev_out.replace('\r', '').split('\n')[0]
    test_result = test_out.replace('\r', '').split('\n')[0]
    when = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    create_submission_model = Submission(
        challenge = challenge,
        submitter = submitter,
        description = description,
        dev_result = dev_result,
        test_result = test_result,
        when = when,
    )
    db.add(create_submission_model)
    db.commit()
    return {"success": True, "submission": description, "message": "Submission added successfully"}

@router.get("/get-metrics")
async def get_metrics(db: db_dependency):
    result = []
    if len(db.query(Metric).all()) == 0:
        basic_metrics = [Metric(name = "Accuracy"), Metric(name = "Recall"), Metric(name = "Precision"), Metric(name = "F-score")]
        for metric in basic_metrics:
            db.add(metric)
            db.commit()
    for metric in db.query(Metric).all():
        result.append({
            "id": metric.id,
            "name": metric.name,
        })
    return result

@router.get("/{challenge}/all-entries")
async def get_all_entries(db: db_dependency, challenge: str):
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