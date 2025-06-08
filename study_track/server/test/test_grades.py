from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from database import SessionLocal, get_db
from main import app  # 假设你的FastAPI应用在main.py中
from models import Grade, Course, SemesterGPA, Student
from schemas import GradeInput

def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_database():
    # 在每个测试之前开始事务
    db = SessionLocal()
    db.begin()
    yield
    # 在每个测试之后回滚事务
    db.rollback()
    db.close()


def test_insert_grade_success():
    # 假设课程和学生已存在
    grade_data = {
        "student_no": "09022124",
        "course_name": "数据分析导论",
        "semester": "2024春",
        "score": 90.0
    }

    response = client.post("/insert_grade", json=grade_data)

    assert response.status_code == 200
    assert response.json() == {"msg": "success"}

def test_insert_grade_course_not_found():
    grade_data = {
        "student_no": "09022124",
        "course_name": "不存在的课程",
        "semester": "2023-2024-1",
        "score": 90.0
    }

    response = client.post("/insert_grade", json=grade_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found"

def test_insert_grade_already_exists():
    # 先插入一条成绩记录
    grade_data = {
        "student_no": "09022125",
        "course_name": "人工智能基础",
        "semester": "2023秋",
        "score": 90.0
    }
    client.post("/insert_grade", json=grade_data)

    # 再次插入相同的成绩记录
    response = client.post("/insert_grade", json=grade_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Grade already exists for this student, course, and semester"
def test_get_student_grades_success():
    # 假设学生成绩记录已存在
    student_no = "09022124"

    response = client.get(f"/grades/{student_no}")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_student_grades_not_found():
    student_no = "99999999"

    response = client.get(f"/grades/{student_no}")

    assert response.status_code == 404
    assert response.json()["detail"] == "未找到该学生的成绩记录"
def test_get_semester_gpas_success():
    # 假设学生的学期 GPA 记录已存在
    student_no = "09022124"

    response = client.get(f"/semester_gpa/{student_no}")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_semester_gpas_not_found():
    student_no = "99999999"

    response = client.get(f"/semester_gpa/{student_no}")

    assert response.status_code == 404
    assert response.json()["detail"] == "未找到该学生的学期 GPA 记录"