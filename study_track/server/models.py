from sqlalchemy import Column, String, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from database import Base


# 学生模型
class Student(Base):
    __tablename__ = "students"
    student_no = Column(String, primary_key=True, index=True)
    name = Column(String)
    major = Column(String)
    grade = Column(String)
    username = Column(String)
    school = Column(String)
    college = Column(String)
    password = Column(String)

    grades = relationship("Grade", back_populates="student")


class Course(Base):
    __tablename__ = 'courses'
    course_code = Column(String, primary_key=True)
    course_name = Column(String)
    credit = Column(Float, nullable=False)


# 成绩模型
class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, index=True)
    student_no = Column(String, ForeignKey('students.student_no'))
    course_code = Column(String, ForeignKey('courses.course_code'))
    score = Column(Float)
    semester = Column(String)

    student = relationship("Student", back_populates="grades")
    course = relationship("Course")


class SemesterGPA(Base):
    __tablename__ = "semester_gpa"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_no = Column(String(20), nullable=False)
    semester = Column(String(15), nullable=False)
    semester_gpa = Column(Float, nullable=False)


class StudyAdvice(Base):
    __tablename__ = "study_advices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_no = Column(String(20), ForeignKey("students.student_no"))
    advice = Column(Text)