from fastapi import APIRouter, Depends, UploadFile, File
from database.models import Metric
from sqlalchemy.orm import Session
from typing import Annotated
import evaluation.evaluation_helper as evaluation_helper

router = APIRouter(
    prefix="/evaluation",
    tags=['evaluation']
)
