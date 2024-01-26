from fastapi import APIRouter, Depends, UploadFile, File
from data.models import Metric
from data.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
import evaluation.evaluation_helper as evaluation_helper

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

@router.post("/submit")
async def submit(db: db_dependency, submission_file:UploadFile = File(...)):
    result = []
    evaluation_helper.check_file_extension(submission_file)
    temp_zip_path = await evaluation_helper.save_zip_file(submission_file)
    challenge_folder_name = await evaluation_helper.extract_submission(temp_zip_path)
    return result

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