from typing import Literal

from pydantic import BaseModel
from enum import Enum


class RoleEnum(str, Enum):
    teacher = "teacher"
    student = "student"


class UserBase(BaseModel):
    username: str
    email: str
    identity: RoleEnum


class UserCreate(UserBase):
    password: str


class TeacherBase(UserBase):
    employee_id: int


class TeacherCreate(TeacherBase):
    password: str


class UserBase(UserBase):
    student_id: int


class StudentCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    password: str = None
    email: str = None
    identity: RoleEnum = None


class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True


class Teacher(User):
    employee_id: int

    class Config:
        orm_mode = True

class Student(User):
    student_id: int

    class Config:
        orm_mode = True