from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.models.job import AuditLog
from backend.services.aws_service import scan_orphaned_resources, delete_resources

router = APIRouter()


@router.get("/scan")
def scan_resources(region: str = "us-east-1", db: Session = Depends(get_db)):
    result = scan_orphaned_resources(region)
    log = AuditLog(event_type="janitor_scan", details={"region": region, "found": len(result)})
    db.add(log)
    db.commit()
    return {"region": region, "orphaned_resources": result}


@router.delete("/clean")
def clean_resources(resource_ids: list[str], region: str = "us-east-1", db: Session = Depends(get_db)):
    result = delete_resources(resource_ids, region)
    log = AuditLog(event_type="janitor_clean", details={"region": region, "deleted": resource_ids})
    db.add(log)
    db.commit()
    return result
