from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import Column, Integer, String, JSON, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# SQLAlchemy Model
class Submission(Base):
    """数据库模型"""
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, nullable=False)
    user_id= Column(Integer, nullable=False)
    answer_sql = Column(String, nullable=False)
    result = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



    def __repr__(self):
        return f"<Submission(result={self.result}, problem_id='{self.problem_id}', answer_sql='{self.answer_sql}')>"