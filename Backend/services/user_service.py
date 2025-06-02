from sqlalchemy.orm import Session
from Backend.models.user import User, Teacher, Student, RoleEnum
from Backend.schemas.user import UserCreate, UserUpdate, TeacherCreate, StudentCreate
from Backend.utils.password_utils import hash_password, verify_password


def get_user_by_name(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, password=user.password, email=user.email, identity=user.identity)
    db_user.password = hash_password(db_user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_teacher(db: Session, teacher: TeacherCreate):
    """
    创建老师用户，处理密码哈希和老师特有字段（工号）。
    """
    hashed_password = hash_password(teacher.password)
    db_teacher = Teacher(
        username=teacher.username,
        password=hashed_password,
        email=teacher.email,
        identity=RoleEnum("teacher"),       # identity 与 polymorphic_identity 保持一致
        employee_id=teacher.employee_id
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


def create_student(db: Session, student: StudentCreate):
    """
    创建学生用户，处理密码哈希和学生特有字段（学号）。
    """
    hashed_password = hash_password(student.password)
    db_student = Student(
        username=student.username,
        password=hashed_password,
        email=student.email,
        identity=RoleEnum("student"),       # identity 与 polymorphic_identity 保持一致
        student_id=student.student_id
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_user(db: Session, user_id: str, user_update: UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    if user_update.password:
        db_user.password = hash_password(user_update.password)
    if user_update.email:
        db_user.email = user_update.email
    if user_update.identity:
        db_user.identity = user_update.identity
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_by_id(db: Session, user_id: str):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user
