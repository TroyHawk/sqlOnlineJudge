import asyncio

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend import schemas
from Backend.database import SessionLocal
from Backend.services import judge_service
from Backend.utils.auth_utils import get_current_user
from Backend.models.user import User as UserModel

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=schemas.submission.Submission)
def create_submission(submission: schemas.submission.SubmissionCreate, db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user),):
    # current_user: UserModel = Depends(get_current_user)
    submission.user_id = current_user.id
    result = asyncio.run(judge_service.create_submission(db, submission))
    return result