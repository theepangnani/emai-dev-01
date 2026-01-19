from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.students import router as students_router
from app.routes.teachers import router as teachers_router

app = FastAPI(title="EMAI API")

app.include_router(health_router)
app.include_router(students_router)
app.include_router(teachers_router)
