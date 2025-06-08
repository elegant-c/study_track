from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Student
from schemas import UserInfo, UpdateUserInfo
from database import get_db

router = APIRouter()


# 获取用户信息
@router.get("/get_user_info/{student_no}", response_model=UserInfo)
def get_user_info(student_no: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_no == student_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# 更新用户信息
@router.put("/update_user_info/{student_no}")
def update_user_info(student_no: str, updated_data: UpdateUserInfo, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_no == student_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = updated_data.name
    student.username = updated_data.username
    student.school = updated_data.school
    student.college = updated_data.college
    student.major = updated_data.major

    db.commit()
    return {"message": "User info updated successfully"}
