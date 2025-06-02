from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend import schemas
from Backend.database import SessionLocal
from Backend.services import user_service

router = APIRouter()


# 获取数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/teacher", response_model=schemas.user.Teacher)
def create_teacher(teacher: schemas.user.TeacherCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    db_user = user_service.get_user_by_username(db, teacher.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    # 交给 service 层处理老师特有逻辑（如保存工号）
    created_teacher = user_service.create_teacher(db, teacher)
    return created_teacher


@router.post("/", response_model=schemas.user.User)
def create_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_name(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_service.create_user(db, user)


@router.get("/{username}", response_model=schemas.user.User)
def read_user(username: str, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_name(db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=list[schemas.user.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.get_users(db, skip=skip, limit=limit)


@router.put("/{username}", response_model=schemas.user.User)
def update_user(username: str, user_update: schemas.user.UserUpdate, db: Session = Depends(get_db)):
    db_user = user_service.update_user(db, username, user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{username}", response_model=schemas.user.User)
def delete_user(username: str, db: Session = Depends(get_db)):
    db_user = user_service.delete_user(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
