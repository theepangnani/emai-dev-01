from pydantic import BaseModel
from typing import Optional, List

class StudentCreate(BaseModel):
    name: str
    grade: str
    attendancePct: Optional[float] = None
    averageGrade: Optional[float] = None
    missedSubmissions30d: Optional[int] = 0

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    grade: Optional[str] = None
    attendancePct: Optional[float] = None
    averageGrade: Optional[float] = None
    missedSubmissions30d: Optional[int] = None

class StudentOut(BaseModel):
    id: str
    name: str
    grade: str
    attendancePct: Optional[float] = None
    averageGrade: Optional[float] = None
    missedSubmissions30d: Optional[int] = 0
    riskScore: float = 0.0
    recommendedActions: List[str] = []
