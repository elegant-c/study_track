from pydantic import BaseModel, validator


class ScoreItem(BaseModel):
    course_name: str
    score: float


class StudyAdviceRequest(BaseModel):
    student_no: str


class GPARequest(BaseModel):
    student_no: str


class StudyAdvicePayload(BaseModel):
    major: str
    grade: str
    scores: dict


class GradeInput(BaseModel):
    student_no: str
    course_name: str
    semester: str
    score: float


class GradeOutput(BaseModel):
    course_code: str
    course_name: str
    semester: str
    score: float
    credit: float

    class Config:
        # orm_mode = True
        from_attributes = True

class UserInfo(BaseModel):
    name: str
    username: str
    school: str
    college: str
    major: str

    class Config:
        from_attributes = True


class UpdateUserInfo(BaseModel):
    name: str
    username: str
    school: str
    college: str
    major: str


class LoginRequest(BaseModel):
    student_no: str
    password: str


class RegisterRequest(BaseModel):
    name: str
    student_no: str
    grade: str
    username: str
    major: str
    college: str
    school: str
    password: str
    confirm_password: str

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("密码不一致")
        return v


class SemesterGPAOut(BaseModel):
    semester: str
    semester_gpa: float

    class Config:
        from_attributes = True
