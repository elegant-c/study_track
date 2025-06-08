from fastapi import APIRouter, HTTPException, Depends
from database import SessionLocal
from models import Grade, Course, SemesterGPA
from gpa_utils import calculate_gpa
from schemas import GradeInput, GradeOutput, SemesterGPAOut
from sqlalchemy.orm import Session
from database import get_db
from typing import List


router = APIRouter()


@router.post("/insert_grade")
def insert_grade(grade_data: GradeInput):
    db = SessionLocal()

    try:
        # 查找课程
        course = db.query(Course).filter(Course.course_name == grade_data.course_name).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        course_code = course.course_code

        # ===== 新增：检查成绩是否已存在 =====
        existing_grade = db.query(Grade).filter_by(
            student_no=grade_data.student_no,
            course_code=course_code,
            semester=grade_data.semester
        ).first()

        if existing_grade:
            raise HTTPException(status_code=400, detail="Grade already exists for this student, course, and semester")

        # 插入成绩
        new_grade = Grade(
            student_no=grade_data.student_no,
            course_code=course_code,
            semester=grade_data.semester,
            score=grade_data.score
        )
        db.add(new_grade)
        db.commit()

        # 获取该学生该学期所有成绩
        all_grades = db.query(Grade).filter(
            Grade.student_no == grade_data.student_no,
            Grade.semester == grade_data.semester
        ).all()

        # 获取所有涉及到的课程信息
        course_codes = [g.course_code for g in all_grades]
        courses = {
            c.course_code: c for c in db.query(Course).filter(
                Course.course_code.in_(course_codes)
            ).all()
        }

        # 构建 (grade, course) 列表用于 GPA 计算
        grades_with_credit = [
            (g, courses[g.course_code])
            for g in all_grades if g.course_code in courses
        ]

        gpa = calculate_gpa(grades_with_credit)

        # 插入或更新 semester_gpa 表
        existing_gpa = db.query(SemesterGPA).filter_by(
            student_no=grade_data.student_no,
            semester=grade_data.semester
        ).first()

        if existing_gpa:
            existing_gpa.semester_gpa = gpa
        else:
            new_semester_gpa = SemesterGPA(
                student_no=grade_data.student_no,
                semester=grade_data.semester,
                semester_gpa=gpa
            )
            db.add(new_semester_gpa)

        db.commit()

        return {"msg": "success"}

    finally:
        db.close()



@router.get("/grades/{student_no}", response_model=list[GradeOutput])
def get_student_grades(student_no: str, db: Session = Depends(get_db)):
    # 联表查询 grades 和 courses
    grades_with_courses = (
        db.query(Grade, Course.course_name)
        .join(Course, Grade.course_code == Course.course_code)
        .filter(Grade.student_no == student_no)
        .all()
    )

    if not grades_with_courses:
        raise HTTPException(status_code=404, detail="未找到该学生的成绩记录")

    # 将查询结果格式化为 GradeOutput 结构
    result = []
    for grade, course_name in grades_with_courses:
        result.append({
            "course_code": grade.course_code,
            "course_name": course_name,
            "semester": grade.semester,
            "score": grade.score,
            "credit": grade.course.credit  # 如果不需要 credit 可移除
        })

    return result


@router.get("/semester_gpa/{student_no}", response_model=List[SemesterGPAOut])
def get_semester_gpas(student_no: str, db: Session = Depends(get_db)):
    # 查询所有学期 GPA
    gpa_records = db.query(SemesterGPA).filter(
        SemesterGPA.student_no == student_no
    ).all()

    if not gpa_records:
        raise HTTPException(
            status_code=404,
            detail="未找到该学生的学期 GPA 记录"
        )

    return gpa_records
