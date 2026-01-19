from fastapi import Header, HTTPException
import firebase_admin
from firebase_admin import auth as fb_auth, credentials
from app.config import settings

_initialized = False

def _init_firebase():
    global _initialized
    if _initialized:
        return
    # In Cloud Run, ADC works for many GCP services. Firebase Admin token verification
    # typically works with default creds if properly configured.
    firebase_admin.initialize_app()
    _initialized = True

def require_auth(authorization: str | None = Header(default=None)):
    if not settings.auth_required:
        return {"uid": "demo", "role": "teacher"}

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.replace("Bearer ", "").strip()
    _init_firebase()

    try:
        decoded = fb_auth.verify_id_token(token)
        role = decoded.get("role", "teacher")
        return {"uid": decoded.get("uid"), "email": decoded.get("email"), "role": role}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
