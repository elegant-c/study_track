import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
import os

# 导入你的FastAPI应用和模型
from main import app  # 假设你的FastAPI应用在main.py中
from database import get_db, Base, SessionLocal
from models import Student
from security import verify_password  # 确保导入verify_password


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


def test_register_success():
    test_data = {
        "name": "钱七",
        "student_no": "20230006",
        "grade": "2023",
        "username": "qianqi",
        "major": "数据科学",
        "college": "统计学院",
        "school": "复旦大学",
        "password": "correctpass",
        "confirm_password": "correctpass"
    }

    response = client.post("/register", json=test_data)

    assert response.status_code == 200
    assert response.json() == {"message": "注册成功"}

    # 验证用户是否真正存入数据库
    db = SessionLocal()
    user = db.query(Student).filter(Student.student_no == test_data["student_no"]).first()
    db.close()
    assert user is not None
    assert user.username == test_data["username"]
    assert verify_password(test_data["password"], user.password)


def test_register_duplicate_student_no():
    # 第一次注册
    test_data1 = {
        "name": "钱七",
        "student_no": "20230006",
        "grade": "2023",
        "username": "qianqi1",
        "major": "数据科学",
        "college": "统计学院",
        "school": "复旦大学",
        "password": "correctpass",
        "confirm_password": "correctpass"
    }
    client.post("/register", json=test_data1)

    # 尝试用相同的学号注册
    test_data2 = {
        "name": "钱八",
        "student_no": "20230006",  # 相同的学号
        "grade": "2023",
        "username": "qianqi2",
        "major": "数据科学",
        "college": "统计学院",
        "school": "复旦大学",
        "password": "correctpass",
        "confirm_password": "correctpass"
    }

    response = client.post("/register", json=test_data2)

    assert response.status_code == 400
    assert response.json()["detail"] == "学号或用户名已被注册"


def test_register_password_mismatch():
    test_data = {
        "name": "钱七",
        "student_no": "20230007",
        "grade": "2023",
        "username": "qianqi",
        "major": "数据科学",
        "college": "统计学院",
        "school": "复旦大学",
        "password": "correctpass",
        "confirm_password": "wrongpass"  # 不匹配的密码
    }

    response = client.post("/register", json=test_data)

    assert response.status_code == 422  # 验证错误通常返回422
    assert "密码不一致" in response.json()["detail"][0]["msg"]


def test_login_success():
    # 先注册用户
    test_data = {
        "name": "张三",
        "student_no": "20230008",
        "grade": "2023",
        "username": "zhangsan",
        "major": "数据科学",
        "college": "统计学院",
        "school": "复旦大学",
        "password": "correctpass",
        "confirm_password": "correctpass"
    }
    response = client.post("/register", json=test_data)
    assert response.status_code == 200
    assert response.json() == {"message": "注册成功"}
    # 测试登录
    login_data = {
        "student_no": "20230008",
        "password": "correctpass"
    }

    response = client.post("/login", json=login_data)

    assert response.status_code == 200
    assert response.json() == {"message": "登录成功"}


def test_login_wrong_password():
    # 先注册用户
    test_data = {
        "name": "李四",
        "student_no": "20230009",
        "grade": "2023",
        "username": "lisi",
        "major": "数据科学",
        "college": "统计学院",
        "school": "复旦大学",
        "password": "correctpass",
        "confirm_password": "correctpass"
    }
    client.post("/register", json=test_data)

    # 测试错误的密码
    login_data = {
        "student_no": "20230009",
        "password": "wrongpass"  # 错误的密码
    }

    response = client.post("/login", json=login_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "密码错误"


def test_login_nonexistent_student():
    login_data = {
        "student_no": "99999999",  # 不存在的学号
        "password": "anypassword"
    }

    response = client.post("/login", json=login_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "学号不存在"