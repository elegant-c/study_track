from fastapi.testclient import TestClient
from unittest.mock import MagicMock, create_autospec
import pytest
from sqlalchemy.orm import Session
from main import app
from sqlalchemy.exc import DataError
from database import get_db

# 创建测试客户端fixture
@pytest.fixture
def client():
    return TestClient(app)


# 创建mock_db fixture
@pytest.fixture
def mock_db(mocker):
    # 创建自动模拟的Session对象
    mock_session = create_autospec(Session, instance=True)
    # 模拟数据库依赖
    mocker.patch('database.get_db', return_value=mock_session)
    return mock_session


# 创建模拟学生对象的辅助函数
def create_mock_student(student_no: str):
    mock_student = MagicMock()
    mock_student.student_no = student_no
    mock_student.name = "程曼佳" if student_no == "09022124" else "胡溦溦"
    mock_student.username = "2542077205@qq.com" if student_no == "09022124" else "1253550373@qq.com"
    mock_student.school = "SEU"
    mock_student.college = "计软智学院"
    mock_student.major = "计算机科学与技术"
    mock_student.grade = "2022"
    mock_student.password = "$2b$12$9QuyVKeNSVw"
    return mock_student


# 测试获取用户信息 - 学生存在
def test_get_user_info_success(client, mock_db):
    # 创建模拟学生对象
    mock_student = create_mock_student("09022124")
    # 设置数据库查询返回
    mock_db.query.return_value.filter.return_value.first.return_value = mock_student

    # 执行请求
    response = client.get("/get_user_info/09022124")

    # 验证结果
    assert response.status_code == 200
    data = response.json()

    # 验证响应包含正确的字段值
    assert data["name"] == "程曼佳"
    assert data["username"] == "2542077205@qq.com"
    assert data["school"] == "SEU"
    assert data["college"] == "计软智学院"
    assert data["major"] == "计算机科学与技术"


# 测试获取用户信息 - 学生不存在
def test_get_user_info_not_found(client, mock_db):
    # 模拟找不到学生
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # 执行请求
    response = client.get("/get_user_info/09022121")

    # 验证结果
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


# 测试更新用户信息 - 成功
def test_update_user_info_success(client, mock_db):
    # 创建模拟学生对象
    mock_student = create_mock_student("09022125")
    # 设置数据库查询返回
    mock_db.query.return_value.filter.return_value.first.return_value = mock_student

    # 更新数据
    update_data = {
        "name": "胡溦溦更新",
        "username": "new_email@qq.com",
        "school": "SEU更新",
        "college": "计软智学院更新",
        "major": "软件工程"
    }

    # 执行请求
    response = client.put("/update_user_info/09022125", json=update_data)

    # 验证结果
    assert response.status_code == 200
    assert response.json()["message"] == "User info updated successfully"

    # 验证数据库更新被调用
    # assert mock_db.commit.called
    # 验证学生对象属性被更新

    # assert mock_student.name == "胡溦溦更新"
    # assert mock_student.username == "new_email@qq.com"
    # assert mock_student.school == "SEU更新"
    # assert mock_student.college == "计软智学院更新"
    # assert mock_student.major == "软件工程"


# 测试更新用户信息 - 学生不存在
def test_update_user_info_not_found(client, mock_db):
    # 模拟找不到学生
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # 更新数据
    update_data = {
        "name": "胡溦溦更新",
        "username": "new_email@qq.com",
        "school": "SEU更新",
        "college": "计软智学院更新",
        "major": "软件工程"
    }

    # 执行请求
    response = client.put("/update_user_info/99999999", json=update_data)

    # 验证结果
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"
    # 验证数据库未提交
    # assert not mock_db.commit.called


# 测试响应模型结构
def test_get_user_info_response_model(client, mock_db):
    # 创建模拟学生对象
    mock_student = create_mock_student("09022124")
    # 设置数据库查询返回
    mock_db.query.return_value.filter.return_value.first.return_value = mock_student

    # 执行请求
    response = client.get("/get_user_info/09022124")

    # 验证结果
    assert response.status_code == 200
    data = response.json()

    # 确认响应只包含 UserInfo 模型的字段
    expected_fields = {"name", "username", "school", "college", "major"}
    assert set(data.keys()) == expected_fields

    # 确认所有字段都是字符串类型
    for field in expected_fields:
        assert isinstance(data[field], str)