from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProblemBase(BaseModel):
    problem_name: str
    description: Optional[str] = None
    difficulty: Optional[str] = None
    test_cases: Optional[str] = None


class ProblemCreate(ProblemBase):
    pass


class ProblemUpdate(BaseModel):
    problem_name: str = None
    description: str = None
    difficulty: str = None
    test_cases: str = None


class Problem(ProblemBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
