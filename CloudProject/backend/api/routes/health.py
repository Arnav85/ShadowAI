from fastapi import APIRouter
from sqlalchemy import text
from backend.db.session import engine

router = APIRouter()


@router.get("/health")
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {e}"

    return {
        "status": "ok",
        "api": "cloud-janitor",
        "version": "1.0.0",
        "database": db_status,
    }
