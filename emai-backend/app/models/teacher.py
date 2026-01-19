from pydantic import BaseModel

class TeacherCreate(BaseModel):
    name: str
    schoolId: str

class TeacherOut(BaseModel):
    id: str
    name: str
    schoolId: str
