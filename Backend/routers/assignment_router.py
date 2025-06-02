from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend import schemas
from Backend.database import SessionLocal
from Backend.services import assignment_service

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.assignment.Assignment)
def create_assignment(assignment: schemas.assignment.AssignmentCreate, db: Session = Depends(get_db)):
    return assignment_service.create_assignment(db, assignment)


@router.get("/{assignment_id}", response_model=schemas.assignment.Assignment)
def read_assignment(assignment_id: int, db: Session = Depends(get_db)):
    db_assignment = assignment_service.get_assignment(db, assignment_id)
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return db_assignment


@router.get("/", response_model=list[schemas.assignment.Assignment])
def read_assignments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return assignment_service.get_assignments(db, skip=skip, limit=limit)


@router.put("/{assignment_id}", response_model=schemas.assignment.Assignment)
def update_assignment(assignment_id: int, assignment_update: schemas.assignment.AssignmentUpdate,
                      db: Session = Depends(get_db)):
    db_assignment = assignment_service.update_assignment(db, assignment_id, assignment_update)
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return db_assignment


@router.delete("/{assignment_id}", response_model=schemas.assignment.Assignment)
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    db_assignment = assignment_service.delete_assignment(db, assignment_id)
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return db_assignment
