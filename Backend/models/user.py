from sqlalchemy import Column, String, Enum, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
import enum


class RoleEnum(enum.Enum):
    teacher = "teacher"
    student = "student"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    identity = Column(Enum(RoleEnum), nullable=False)
    __mapper_args__ = {
        'polymorphic_on': identity,
        'polymorphic_identity': 'user'  # 基类的标识，可以是任意值
    }


class Teacher(User):
    __tablename__ = "teachers"
    id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    employee_id = Column(String,  primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': RoleEnum('teacher'),  # 必须与 identity 字段中的值对应
    }


class Student(User):
    __tablename__ = "students"
    id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    student_id = Column(String,  primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': RoleEnum('student'),
    }
