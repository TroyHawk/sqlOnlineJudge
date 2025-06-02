from Backend.database import SessionLocal
from Backend.models.user import RoleEnum
from Backend.services import user_service
import random
import string


def generate_random_string(length):
    # 包含大小写字母和数字
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


db = SessionLocal()

from Backend.schemas import user


def test_add_user(new_user=None):
    if new_user is None:
        new_user = user.UserCreate(username=generate_random_string(10), password='123456',
                                   email=generate_random_string(5),
                                   identity='teacher')
    user_service.create_user(db, new_user)


def test_add_teacher(new_user=None):
    if new_user is None:
        new_user = user.TeacherCreate(employee_id=10680, username=generate_random_string(10), password='123456',
                                      email=generate_random_string(5),
                                      identity='teacher')
    user_service.create_teacher(db, new_user)


def test_add_student(new_user=None):
    if new_user is None:
        new_user = user.StudentCreate(student_id=2024001, username=generate_random_string(10), password='123456',
                                      email=generate_random_string(5),
                                      identity=RoleEnum('student'))
    user_service.create_student(db, new_user)


def test_delete_user(id):
    user_service.delete_user_by_id(db, id)

def test_get_user(id):
    user = user_service.get_user_by_id(db, id)
    print(user)


# test_add_user()
# test_add_teacher()
# test_add_student()
test_delete_user(1)
# test_get_user(2)

