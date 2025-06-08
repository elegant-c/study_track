from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Student, Grade, Course, SemesterGPA
from schemas import StudyAdviceRequest
from services.ai_service import AIService
from crud import save_study_advice
from database import get_db
from schemas import StudyAdviceRequest, GPARequest


router = APIRouter()



@router.post("/ask_llm")
def ask_llm(request: StudyAdviceRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_no == request.student_no).first()
    if not student:
        return {"error": "学生不存在"}

    grades = (
        db.query(Grade, Course)
        .join(Course, Grade.course_code == Course.course_code)
        .filter(Grade.student_no == request.student_no)
        .all()
    )

    scores_dict = {course.course_name: grade.score for grade, course in grades}

    payload = {
        "major": student.major,
        "grade": student.grade,
        "scores": scores_dict
    }

    ai = AIService()
    result = ai.get_study_advice(payload)

    # 如果成功，保存 advice 到数据库
    if result["status"] == "success":
        advice_text = result["advice"]
        save_study_advice(db, request.student_no, advice_text)
        return {"advice": advice_text}

    # 如果失败，返回错误信息
    return {"error": result.get("error", "调用大模型失败")}


@router.post("/predict_gpa")
def predict_gpa(request: GPARequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_no == request.student_no).first()
    if not student:
        return {"error": "学生不存在"}

    semester_gpas = db.query(SemesterGPA).filter(
        SemesterGPA.student_no == request.student_no
    ).all()

    grades = db.query(Grade).filter(
        Grade.student_no == request.student_no
    ).all()

    # 格式化数据
    history_data = {
        "semester_gpa": [
            {"semester": gpa.semester, "gpa": gpa.semester_gpa}
            for gpa in semester_gpas
        ],
        "grades": [
            {
                "course_code": grade.course_code,
                "score": grade.score,
                "semester": grade.semester
            }
            for grade in grades
        ]
    }

    ai = AIService()
    result = ai.predict_gpa(history_data)

    if result["status"] == "success":
        return {"prediction": result["result"]}
    return {"error": result.get("error", "预测失败")}