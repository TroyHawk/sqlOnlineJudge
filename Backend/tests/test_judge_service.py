from Backend.schemas.submission import SubmissionCreate
from Backend.services.judge_service import create_submission, get_submissions
from Backend.database import SessionLocal
import asyncio

db = SessionLocal()


async def test_judge(db, submission: SubmissionCreate = None):
    submission = SubmissionCreate(problem_id=4, user_id=1, answer_sql="SELECT * FROM users WHERE age BETWEEN 20 AND 30")
    await create_submission(db, submission)


asyncio.run(test_judge(db))

def test_get_submissions():
    return get_submissions(db, 1)



# submission = test_get_submissions()[0]
# print(submission.result)
