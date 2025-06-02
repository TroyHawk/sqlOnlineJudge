from sqlalchemy.orm import Session
from Backend.models.assignment import Assignment
from Backend.models.problem import Problem
from Backend.schemas.assignment import AssignmentCreate, AssignmentUpdate


def get_assignment(db: Session, assignment_id: int):
    return db.query(Assignment).filter(Assignment.id == assignment_id).first()


def get_assignments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Assignment).offset(skip).limit(limit).all()


def create_assignment(db: Session, assignment: AssignmentCreate):
    db_assignment = Assignment(
        assignment_name=assignment.assignment_name,
        assignment_description=assignment.assignment_description,
    )
    # 关联题目
    if assignment.problem_ids:
        problems = db.query(Problem).filter(Problem.id.in_(assignment.problem_ids)).all()
        db_assignment.problems = problems
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


def update_assignment(db: Session, assignment_id: int, assignment_update: AssignmentUpdate):
    db_assignment = get_assignment(db, assignment_id)
    if not db_assignment:
        return None
    if assignment_update.assignment_name:
        db_assignment.assignment_name = assignment_update.assignment_name
    if assignment_update.assignment_description:
        db_assignment.assignment_description = assignment_update.assignment_description
    if assignment_update.problem_ids is not None:
        problems = db.query(Problem).filter(Problem.id.in_(assignment_update.problem_ids)).all()
        db_assignment.problems = problems
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


def delete_assignment(db: Session, assignment_id: int):
    db_assignment = get_assignment(db, assignment_id)
    if not db_assignment:
        return None
    db.delete(db_assignment)
    db.commit()
    return db_assignment
