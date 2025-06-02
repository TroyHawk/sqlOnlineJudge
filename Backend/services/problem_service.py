from sqlalchemy.orm import Session
from Backend.models.problem import Problem
from Backend.schemas.problem import ProblemCreate, ProblemUpdate


def get_problem(db: Session, problem_id: int):
    return db.query(Problem).filter(Problem.id == problem_id).first()


def get_problems(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Problem).offset(skip).limit(limit).all()


def create_problem(db: Session, problem: ProblemCreate):
    db_problem = Problem(
        problem_name=problem.problem_name,
        description=problem.description,
        difficulty=problem.difficulty,
        test_cases=problem.test_cases
    )
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem


def update_problem(db: Session, problem_id: int, problem_update: ProblemUpdate):
    db_problem = get_problem(db, problem_id)
    if not db_problem:
        return None
    if problem_update.problem_name:
        db_problem.problem_name = problem_update.problem_name
    if problem_update.description:
        db_problem.description = problem_update.description
    if problem_update.difficulty:
        db_problem.difficulty = problem_update.difficulty
    if problem_update.test_cases:
        db_problem.test_cases = problem_update.test_cases
    db.commit()
    db.refresh(db_problem)
    return db_problem


def delete_problem(db: Session, problem_id: int):
    db_problem = get_problem(db, problem_id)
    if not db_problem:
        return None
    db.delete(db_problem)
    db.commit()
    return db_problem
