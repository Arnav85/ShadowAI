from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional

from backend.db.session import get_db
from backend.models.migration import MigrationJob, MigrationStatus
from backend.models.job import AuditLog
from backend.services.migration_service import run_migration_job, rollback_last_migration

router = APIRouter()


class RunMigrationRequest(BaseModel):
    name: str
    target_db: str
    sql_script: str
    dry_run: bool = True


class RollbackRequest(BaseModel):
    target_db: str


@router.post("/run")
def run_migration(req: RunMigrationRequest, db: Session = Depends(get_db)):
    job = MigrationJob(
        name=req.name,
        target_db=req.target_db,
        sql_script=req.sql_script,
        dry_run=req.dry_run,
        status=MigrationStatus.running,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    result = run_migration_job(job, db)

    log = AuditLog(
        event_type="migration_run",
        details={"job_id": job.id, "name": req.name, "dry_run": req.dry_run, "status": result["status"]},
    )
    db.add(log)
    db.commit()
    return result


@router.post("/rollback")
def rollback_migration(req: RollbackRequest, db: Session = Depends(get_db)):
    result = rollback_last_migration(req.target_db, db)
    log = AuditLog(
        event_type="migration_rollback",
        details={"target_db": req.target_db, "status": result.get("status")},
    )
    db.add(log)
    db.commit()
    return result


@router.get("/history")
def get_history(limit: int = 20, db: Session = Depends(get_db)):
    jobs = (
        db.query(MigrationJob)
        .order_by(MigrationJob.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": j.id,
            "name": j.name,
            "target_db": j.target_db,
            "dry_run": j.dry_run,
            "status": j.status,
            "created_at": str(j.created_at),
            "error": j.error,
        }
        for j in jobs
    ]


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(func.count(MigrationJob.id)).scalar()
    success = db.query(func.count(MigrationJob.id)).filter(MigrationJob.status == MigrationStatus.success).scalar()
    failed = db.query(func.count(MigrationJob.id)).filter(MigrationJob.status == MigrationStatus.failed).scalar()
    return {"total": total, "success": success, "failed": failed}
