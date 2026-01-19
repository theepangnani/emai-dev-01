from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import require_auth
from app.services.firestore import get_db
from app.services.risk import calculate_risk, recommend_actions
from app.services.events import publish_event
from app.models.student import StudentCreate, StudentUpdate, StudentOut

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=dict)
def create_student(payload: StudentCreate, user=Depends(require_auth)):
    db = get_db()
    doc = {
        **payload.model_dump(),
        "riskScore": 0.0,
        "recommendedActions": [],
    }
    ref = db.collection("students").document()
    ref.set(doc)

    publish_event({"eventType": "student_created", "studentId": ref.id})
    return {"id": ref.id}

@router.get("/", response_model=list[StudentOut])
def list_students(user=Depends(require_auth)):
    db = get_db()
    docs = db.collection("students").stream()
    out = []
    forisk = 0
    for d in docs:
        data = d.to_dict()
        out.append(StudentOut(id=d.id, **data))
    return out

@router.patch("/{student_id}", response_model=dict)
def update_student(student_id: str, payload: StudentUpdate, user=Depends(require_auth)):
    db = get_db()
    ref = db.collection("students").document(student_id)
    snap = ref.get()
    if not snap.exists:
        raise HTTPException(status_code=404, detail="Student not found")

    existing = snap.to_dict()
    patch = {k: v for k, v in payload.model_dump().items() if v is not None}
    merged = {**existing, **patch}

    risk = calculate_risk(
        merged.get("attendancePct"),
        merged.get("averageGrade"),
        merged.get("missedSubmissions30d"),
    )
    actions = recommend_actions(risk)

    ref.set({**patch, "riskScore": risk, "recommendedActions": actions}, merge=True)

    publish_event({"eventType": "student_updated", "studentId": student_id, "riskScore": risk})
    return {"id": student_id, "riskScore": risk, "recommendedActions": actions}
