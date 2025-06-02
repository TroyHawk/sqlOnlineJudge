import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 创建数据库连接
engine = create_engine('mysql+pymysql://root:lusini123@localhost:3306/SQLOnlineJudge')
Session = sessionmaker(bind=engine)
session = Session()

from Backend.services import problem_service
from Backend.schemas.problem import  ProblemCreate


# 测试创建问题
def test_create_problem():
    test_cases = [
        {
            "id": 3,
            "description": "查询年龄在20到30之间的用户",
            "init_sql": [
                "DROP TABLE IF EXISTS users",
                "CREATE TABLE users (id INT, name VARCHAR(50), age INT)",
                "INSERT INTO users VALUES (1, 'Alice', 21), (2, 'Bob', 19), (3, 'Charlie', 29), (4, 'Dave', 31)"
            ],
            "answer_sql": "SELECT * FROM users WHERE age BETWEEN 20 AND 30",
            "score": 10
        }
    ]
    pc3 = ProblemCreate(
        problem_name="基础查询——范围过滤",
        description="返回 users 表中 age 在 20 到 30（含）之间的所有记录。",
        difficulty="简单",
        test_cases=json.dumps(test_cases)
    )
    result = problem_service.create_problem(session, pc3)
    print(result)


# 测试获取问题
def test_get_problem(problem_id=1):
    problem = problem_service.get_problem(session, problem_id)
    print(problem)


test_create_problem()

