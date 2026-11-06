from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Numeric,
    DateTime, Text
)
from models.base import Base


def _utcnow():
    return datetime.now(timezone.utc)


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pipeline_name = Column(String(100), nullable=False)
    run_status = Column(String(20), nullable=False)
    records_extracted = Column(Integer, default=0)
    records_transformed = Column(Integer, default=0)
    records_loaded = Column(Integer, default=0)
    error_message = Column(Text)
    started_at = Column(DateTime, nullable=False, default=_utcnow)
    completed_at = Column(DateTime)
    duration_seconds = Column(Numeric(10, 2))

    def to_dict(self):
        return {
            "pipeline_name": self.pipeline_name,
            "run_status": self.run_status,
            "records_extracted": self.records_extracted,
            "records_transformed": self.records_transformed,
            "records_loaded": self.records_loaded,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": float(self.duration_seconds) if self.duration_seconds else None
        }

