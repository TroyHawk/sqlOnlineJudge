from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# 关联表，实现作业和题目的多对多关系
assignment_problem_association = Table(
    'assignment_problem',
    Base.metadata,
    Column('assignment_id', Integer, ForeignKey('assignments.id')),
    Column('problem_id', Integer, ForeignKey('problems.id'))
)


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    assignment_name = Column(String, nullable=False)
    assignment_description = Column(Text)
    problems = relationship("Problem", secondary=assignment_problem_association, backref="assignments")
