# app/schemas/auth.py
from pydantic import BaseModel
from typing import Optional
from enum import Enum


class RoleEnum(str, Enum):
    teacher = "teacher"
    student = "student"


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    id: int
    username: str
    email: str
    identity: RoleEnum
    token: str

    class Config:
        orm_mode = True
