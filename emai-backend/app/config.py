from pydantic import BaseModel
import os

class Settings(BaseModel):
    gcp_project: str = os.getenv("GCP_PROJECT", "")
    events_topic: str = os.getenv("EVENTS_TOPIC", "")  # e.g. "emai-events"
    auth_required: bool = os.getenv("AUTH_REQUIRED", "false").lower() == "true"

settings = Settings()
