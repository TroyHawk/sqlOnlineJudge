from pydantic import BaseModel
from typing import List, Optional

class AssignmentBase(BaseModel):
    assignment_name: str
    assignment_description: Optional[str] = None
    problem_ids: List[int] = []

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(BaseModel):
    assignment_name: str = None
    assignment_description: str = None
    problem_ids: List[int] = None

class Assignment(AssignmentBase):
    id: int

    class Config:
        orm_mode = True
