from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum
from sqlalchemy.sql import func
import enum

from backend.db.session import Base


class MigrationStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    success = "success"
    failed = "failed"
    rolled_back = "rolled_back"


class MigrationJob(Base):
    __tablename__ = "migration_jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    target_db = Column(String(100), nullable=False)
    sql_script = Column(Text, nullable=False)
    dry_run = Column(Boolean, default=False)
    status = Column(Enum(MigrationStatus), default=MigrationStatus.pending, nullable=False)
    output = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    executed_by = Column(String(100), default="api")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
