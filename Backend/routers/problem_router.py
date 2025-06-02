from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend import schemas
from Backend.database import SessionLocal
from Backend.services import problem_service

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.problem.Problem)
def create_problem(problem: schemas.problem.ProblemCreate, db: Session = Depends(get_db)):
    return problem_service.create_problem(db, problem)


@router.get("/{problem_id}", response_model=schemas.problem.Problem)
def read_problem(problem_id: int, db: Session = Depends(get_db)):
    db_problem = problem_service.get_problem(db, problem_id)
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return db_problem


@router.get("", response_model=list[schemas.problem.Problem])
def read_problems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return problem_service.get_problems(db, skip=skip, limit=limit)


@router.put("/{problem_id}", response_model=schemas.problem.Problem)
def update_problem(problem_id: int, problem_update: schemas.problem.ProblemUpdate, db: Session = Depends(get_db)):
    db_problem = problem_service.update_problem(db, problem_id, problem_update)
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return db_problem


@router.delete("/{problem_id}", response_model=schemas.problem.Problem)
def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    db_problem = problem_service.delete_problem(db, problem_id)
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return db_problem
