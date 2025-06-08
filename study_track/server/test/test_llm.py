from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import pytest
from sqlalchemy.orm import Session

# 导入你的 FastAPI 应用实例
from main import app
from database import get_db
from models import Student, SemesterGPA, Grade, Course


# 创建 client fixture
@pytest.fixture
def client():
    return TestClient(app)


# 创建 mock_db fixture
@pytest.fixture
def mock_db(mocker):
    # 创建模拟数据库会话
    mock_session = MagicMock()
    # 模拟 get_db 依赖
    mocker.patch('database.get_db', return_value=mock_session)
    return mock_session


# 测试 /ask_llm 端点 - 成功
def test_ask_llm_success(client, mock_db):
    # 模拟数据库返回学生数据
    mock_student = MagicMock()
    mock_student.major = "计算机科学与技术"
    mock_student.grade = "2022"
    mock_db.query.return_value.filter.return_value.first.return_value = mock_student

    # 模拟成绩数据
    mock_grade = MagicMock()
    mock_grade.score = 85  # 使用数值类型
    mock_course = MagicMock()
    mock_course.course_name = "高等数学"

    # 设置成绩查询返回
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = [
        (mock_grade, mock_course)
    ]

    # 执行请求
    response = client.post("/ask_llm", json={"student_no": "09022125"})

    # 验证状态码为200
    assert response.status_code == 200


# 测试 /ask_llm 端点 - 学生不存在
def test_ask_llm_student_not_found(client, mock_db):
    # 模拟学生不存在
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # 执行请求
    response = client.post("/ask_llm", json={"student_no": "99999999"})

    # 验证状态码为200
    assert response.status_code == 200


# 测试 /ask_llm 端点 - 无成绩数据
def test_ask_llm_no_grades(client, mock_db):
    # 模拟数据库返回学生数据
    mock_student = MagicMock()
    mock_student.major = "计算机科学与技术"
    mock_student.grade = "2022"
    mock_db.query.return_value.filter.return_value.first.return_value = mock_student

    # 模拟无成绩数据
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = []

    # 执行请求
    response = client.post("/ask_llm", json={"student_no": "09022125"})

    # 验证状态码为200
    assert response.status_code == 200


# 绩点预测 - 成功
def test_predict_gpa_success(client, mock_db):
    # 模拟数据库返回学生数据
    mock_student = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_student

    # 模拟学期GPA数据
    mock_semester_gpas = [
        MagicMock(semester="2022秋季", semester_gpa=3.5),
        MagicMock(semester="2023春季", semester_gpa=3.7)
    ]

    # 模拟成绩数据
    mock_grades = [
        MagicMock(course_code="CS101", score=85, semester="2022秋季"),
        MagicMock(course_code="MATH202", score=90, semester="2023春季")
    ]

    # 设置查询返回
    mock_db.query.return_value.filter.return_value.all.side_effect = [
        mock_semester_gpas,  # SemesterGPA查询返回
        mock_grades  # Grade查询返回
    ]

    # 执行请求
    response = client.post("/predict_gpa", json={"student_no": "09022125"})

    # 验证状态码为200
    assert response.status_code == 200


# 绩点预测 - 学生不存在
def test_predict_gpa_student_not_found(client, mock_db):
    # 模拟学生不存在
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # 执行请求
    response = client.post("/predict_gpa", json={"student_no": "99999999"})

    # 验证状态码为200
    assert response.status_code == 200


# 绩点预测 - 无历史数据
def test_predict_gpa_no_history(client, mock_db):
    # 模拟数据库返回学生存在
    mock_student = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_student

    # 模拟无GPA历史数据
    mock_db.query.return_value.filter.return_value.all.side_effect = [
        [],  # SemesterGPA查询返回空
        []  # Grade查询返回空
    ]

    # 执行请求
    response = client.post("/predict_gpa", json={"student_no": "09022125"})

    # 验证状态码为200
    assert response.status_code == 200


# 绩点预测 - 数据结构验证
def test_predict_gpa_data_structure(client, mock_db):
    # 模拟数据库返回
    mock_student = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_student

    # 创建模拟数据
    mock_gpa1 = MagicMock(semester="2022秋季", semester_gpa=3.5)
    mock_gpa2 = MagicMock(semester="2023春季", semester_gpa=3.7)
    mock_grades = [
        MagicMock(course_code="CS101", score=85, semester="2022秋季"),
        MagicMock(course_code="MATH202", score=90, semester="2023春季")
    ]

    # 设置查询返回
    mock_db.query.return_value.filter.return_value.all.side_effect = [
        [mock_gpa1, mock_gpa2],  # SemesterGPA
        mock_grades  # Grades
    ]

    # 执行请求
    response = client.post("/predict_gpa", json={"student_no": "09022125"})

    # 验证状态码为200
    assert response.status_code == 200
