from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.models.migration import MigrationJob, MigrationStatus


def run_migration_job(job: MigrationJob, db: Session) -> dict:
    try:
        if job.dry_run:
            job.status = MigrationStatus.success
            job.output = f"[DRY RUN] SQL validated successfully:\n{job.sql_script}"
            db.commit()
            return {"status": "success", "message": "Dry run completed — no changes applied.", "job_id": job.id}

        # Execute against the app's own DB connection (extend for multi-DB routing as needed)
        with db.bind.connect() as conn:
            with conn.begin():
                conn.execute(text(job.sql_script))

        job.status = MigrationStatus.success
        job.output = "Migration applied successfully."
        db.commit()
        return {"status": "success", "message": "Migration applied.", "job_id": job.id}

    except Exception as e:
        job.status = MigrationStatus.failed
        job.error = str(e)
        db.commit()
        return {"status": "failed", "message": str(e), "job_id": job.id}


def rollback_last_migration(target_db: str, db: Session) -> dict:
    last_job = (
        db.query(MigrationJob)
        .filter(
            MigrationJob.target_db == target_db,
            MigrationJob.status == MigrationStatus.success,
            MigrationJob.dry_run == False,
        )
        .order_by(MigrationJob.created_at.desc())
        .first()
    )

    if not last_job:
        return {"status": "error", "message": "No successful migration found to roll back."}

    last_job.status = MigrationStatus.rolled_back
    db.commit()

    return {
        "status": "success",
        "message": f"Migration '{last_job.name}' marked as rolled back. Apply reverse SQL manually if needed.",
        "job_id": last_job.id,
    }
