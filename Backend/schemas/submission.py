from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SubmissionBase(BaseModel):
    problem_id: Optional[int] = None
    user_id: Optional[int] = None
    answer_sql: Optional[str] = None
    result:Optional[str] = None


class SubmissionCreate(SubmissionBase):
    pass


class Submission(SubmissionBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
