from sqlalchemy.orm import Session
from models import Student, Grade, StudyAdvice


# 查询学生信息和成绩
# def get_student_info(db: Session, student_id: str):
#     student = db.query(Student).filter(Student.student_id == student_id).first()
#     grades = db.query(Grade).filter(Grade.student_id == student_id).all()
#
#     if student is None:
#         return None, None
#
#     grades_data = [{"course_code": grade.course_code, "score": grade.score, "semester": grade.semester} for grade in
#                    grades]
#     return student, grades_data


def save_study_advice(db: Session, student_no: str, advice: str):
    db_advice = StudyAdvice(student_no=student_no, advice=advice)
    db.add(db_advice)
    db.commit()
    db.refresh(db_advice)
    return db_advice

# crud.py 文件中的操作函数



# def get_student_by_student_no(db: Session, student_no: str):
#     return db.query(models.Student).filter(models.Student.student_no == student_no).first()
#
# def update_student_info(db: Session, student_no: str, user_update):
#     db_student = get_student_by_student_no(db, student_no)
#     if db_student:
#         db_student.name = user_update.name
#         db_student.student_no = user_update.username
#         db_student.school = user_update.school
#         db_student.college = user_update.college
#         db_student.major = user_update.major
#         db.commit()
#         db.refresh(db_student)
#         return db_student
#     return None

