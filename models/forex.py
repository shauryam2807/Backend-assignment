from datetime import datetime, date, timezone
from decimal import Decimal
from sqlalchemy import (
    Column, Integer, String, Numeric, Date,
    DateTime, Boolean, UniqueConstraint, Index
)
from models.base import Base


def _utcnow():
    return datetime.now(timezone.utc)


class ForexPair(Base):
    __tablename__ = "forex_pairs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_currency = Column(String(3), nullable=False)
    target_currency = Column(String(3), nullable=False)
    pair_name = Column(String(10), nullable=False)
    source = Column(String(50), default="frankfurter")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (
        UniqueConstraint("base_currency", "target_currency", name="uq_forex_pair"),
    )

    def __repr__(self):
        return f"<ForexPair {self.pair_name}>"

    def to_dict(self):
        return {
            "base_currency": self.base_currency,
            "target_currency": self.target_currency,
            "pair_name": self.pair_name,
            "is_active": self.is_active
        }


class ForexDailyRate(Base):
    __tablename__ = "forex_daily_rates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_currency = Column(String(3), nullable=False)
    target_currency = Column(String(3), nullable=False)
    rate_date = Column(Date, nullable=False)
    exchange_rate = Column(Numeric(18, 8), nullable=False)
    source = Column(String(50), default="frankfurter")
    raw_response_id = Column(String(100))
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (
        UniqueConstraint("base_currency", "target_currency", "rate_date",
                        name="uq_forex_daily_rate"),
        Index("idx_forex_rate_date", "rate_date"),
        Index("idx_forex_rate_pair", "base_currency", "target_currency"),
    )

    def __repr__(self):
        return f"<ForexDailyRate {self.base_currency}/{self.target_currency} {self.rate_date}>"

    def to_dict(self):
        return {
            "base_currency": self.base_currency,
            "target_currency": self.target_currency,
            "date": self.rate_date.isoformat(),
            "rate": float(self.exchange_rate),
            "source": self.source
        }


class ForexOHLCV(Base):
    __tablename__ = "forex_ohlcv_daily"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pair_name = Column(String(10), nullable=False)
    base_currency = Column(String(3), nullable=False)
    target_currency = Column(String(3), nullable=False)
    candle_date = Column(Date, nullable=False)
    open_price = Column(Numeric(18, 8), nullable=False)
    high_price = Column(Numeric(18, 8), nullable=False)
    low_price = Column(Numeric(18, 8), nullable=False)
    close_price = Column(Numeric(18, 8), nullable=False)
    volume = Column(Numeric(24, 2), default=0)
    source = Column(String(50), default="yahoo_finance")
    raw_response_id = Column(String(100))
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (
        UniqueConstraint("pair_name", "candle_date", name="uq_forex_ohlcv"),
        Index("idx_forex_ohlcv_date", "candle_date"),
        Index("idx_forex_ohlcv_pair", "pair_name"),
    )

    def to_dict(self):
        return {
            "symbol": self.pair_name,
            "datetime": self.candle_date.isoformat(),
            "open": f"{float(self.open_price):.5f}",
            "high": f"{float(self.high_price):.5f}",
            "low": f"{float(self.low_price):.5f}",
            "close": f"{float(self.close_price):.5f}",
            "volume": f"{int(self.volume or 0)}",
            "source": self.source,
        }
