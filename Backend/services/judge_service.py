import json

from sqlJudger.core.executor import MySQLExecutor
from sqlJudger.core.judge import SQLJudger
from sqlalchemy.orm import Session
from Backend.models.submission import Submission
from Backend.schemas.submission import SubmissionCreate
from .problem_service import get_problem


async def create_submission(db: Session, submission: SubmissionCreate):
    db_submission = Submission(
        problem_id=submission.problem_id,
        user_id=submission.user_id,
        answer_sql=submission.answer_sql
    )
    problem = get_problem(db, submission.problem_id)
    config = {
        'DB_HOST': 'localhost',
        'DB_PORT': 3306,
        'DB_USER': 'root',
        'DB_PASSWORD': 'lusini123',
        'DB_NAME': 'student'
    }

    # 创建执行器和判题器
    executor = MySQLExecutor(config)
    judger = SQLJudger(executor)

    try:
        # 初始化数据库连接
        await executor.initialize()

        # 评判用户提交的SQL
        result = await judger.judge(submission.answer_sql, json.loads(problem.test_cases))
        db_submission.result = json.dumps(result)
        # 输出结果
        if result["success"]:
            print(f"通过所有测试用例！")
            print(f"得分: {result['score']}/{result['total_score']}")
            print(f"执行时间: {result['execution_time']}秒")
        else:
            print("未通过所有测试用例")
            for case_result in result['test_case_results']:
                if not case_result['success']:
                    print(f"测试用例 {case_result['test_case_id']} 失败:")
                    print(f"错误信息: {case_result['error_message']}")
                else:
                    print(f"答案正确，测试用例 {case_result['test_case_id']} 通过:")
                    print(f"正确答案: {case_result['expected_result']}")
    finally:
        await executor.cleanup()
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


def get_submissions(db: Session, user_id: int):
    return db.query(Submission).filter(Submission.user_id == user_id).all()

