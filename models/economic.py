from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Numeric, Date,
    DateTime, Boolean, Text, UniqueConstraint, Index
)
from models.base import Base


def _utcnow():
    return datetime.now(timezone.utc)


class EconomicIndicator(Base):
    __tablename__ = "economic_indicators"

    id = Column(Integer, primary_key=True, autoincrement=True)
    indicator_id = Column(String(50), nullable=False, unique=True)
    name = Column(String(300), nullable=False)
    description = Column(Text)
    frequency = Column(String(20))
    units = Column(String(100))
    seasonal_adjustment = Column(String(50))
    country = Column(String(50), default="US")
    category = Column(String(100))
    source_agency = Column(String(200))
    source = Column(String(50), default="fred")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    def to_dict(self):
        return {
            "indicator_id": self.indicator_id,
            "name": self.name,
            "frequency": self.frequency,
            "units": self.units,
            "country": self.country,
            "category": self.category
        }


class EconomicIndicatorValue(Base):
    __tablename__ = "economic_indicator_values"

    id = Column(Integer, primary_key=True, autoincrement=True)
    indicator_id = Column(String(50), nullable=False)
    observation_date = Column(Date, nullable=False)
    value = Column(Numeric(20, 4))
    country = Column(String(50), default="US")
    source = Column(String(50), default="fred")
    raw_response_id = Column(String(100))
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (
        UniqueConstraint("indicator_id", "observation_date",
                        name="uq_economic_value"),
        Index("idx_econ_value_date", "observation_date"),
        Index("idx_econ_value_indicator", "indicator_id"),
    )

    def to_dict(self):
        return {
            "indicator_id": self.indicator_id,
            "date": self.observation_date.isoformat(),
            "value": float(self.value) if self.value else None,
            "country": self.country
        }
