from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Student
from schemas import LoginRequest, RegisterRequest
from security import verify_password, get_password_hash

router = APIRouter(tags=["认证"])


@router.post("/register")
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    # 验证学号是否已存在
    existing_user = db.query(Student).filter(
        (Student.student_no == user_data.student_no) |
        (Student.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="学号或用户名已被注册")

    # 创建新用户对象
    new_student = Student(
        name=user_data.name,
        student_no=user_data.student_no,
        grade=user_data.grade,
        username=user_data.username,
        major=user_data.major,
        college=user_data.college,
        school=user_data.school,
        password=get_password_hash(user_data.password)
    )

    try:
        db.add(new_student)
        db.commit()
        return {"message": "注册成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="数据库操作失败")


@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # 查询学生是否存在
    student = db.query(Student).filter(Student.student_no == login_data.student_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="学号不存在")

    # 验证密码
    if not verify_password(login_data.password, student.password):
        raise HTTPException(status_code=401, detail="密码错误")

    return {"message": "登录成功"}