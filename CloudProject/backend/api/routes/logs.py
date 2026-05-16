from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from backend.db.session import get_db
from backend.models.job import AuditLog

router = APIRouter()


@router.get("")
def get_logs(
    limit: int = 50,
    event_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(AuditLog).order_by(AuditLog.created_at.desc())
    if event_type:
        query = query.filter(AuditLog.event_type == event_type)
    logs = query.limit(limit).all()
    return [
        {
            "id": l.id,
            "event_type": l.event_type,
            "actor": l.actor,
            "details": l.details,
            "created_at": str(l.created_at),
        }
        for l in logs
    ]
