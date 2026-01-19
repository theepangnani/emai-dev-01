from fastapi import APIRouter, Depends
from app.middleware.auth import require_auth
from app.services.firestore import get_db
from app.models.teacher import TeacherCreate, TeacherOut

router = APIRouter(prefix="/teachers", tags=["teachers"])

@router.post("/", response_model=dict)
def create_teacher(payload: TeacherCreate, user=Depends(require_auth)):
    db = get_db()
    ref = db.collection("teachers").document()
    ref.set(payload.model_dump())
    return {"id": ref.id}

@router.get("/", response_model=list[TeacherOut])
def list_teachers(user=Depends(require_auth)):
    db = get_db()
    docs = db.collection("teachers").stream()
    return [TeacherOut(id=d.id, **d.to_dict()) for d in docs]
