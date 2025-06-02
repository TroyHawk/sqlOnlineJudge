from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import Column, Integer, String, JSON, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

from sqlJudger.models.TestCase import TestCase

Base = declarative_base()

# SQLAlchemy Model
class Problem(Base):
    """数据库模型"""
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False)
    test_cases = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Problem(id={self.id}, title='{self.problem_name}', difficulty='{self.difficulty}')>"
        
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "difficulty": self.difficulty,
            "test_cases": [TestCase(**eval(case)) for case in self.test_cases]
        }

