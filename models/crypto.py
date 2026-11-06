from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Numeric, Date,
    DateTime, Boolean, Text, UniqueConstraint, Index
)
from models.base import Base


def _utcnow():
    return datetime.now(timezone.utc)


class Cryptocurrency(Base):
    __tablename__ = "cryptocurrencies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    coin_id = Column(String(100), nullable=False, unique=True)
    symbol = Column(String(20), nullable=False)
    name = Column(String(200), nullable=False)
    market_cap_rank = Column(Integer)
    category = Column(String(100))
    description = Column(Text)
    homepage_url = Column(String(500))
    image_url = Column(String(500))
    source = Column(String(50), default="coingecko")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    def to_dict(self):
        return {
            "coin_id": self.coin_id,
            "symbol": self.symbol,
            "name": self.name,
            "market_cap_rank": self.market_cap_rank,
            "category": self.category
        }


class CryptoDailyPrice(Base):
    __tablename__ = "crypto_daily_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    coin_id = Column(String(100), nullable=False)
    price_date = Column(Date, nullable=False)
    price_usd = Column(Numeric(24, 8))
    market_cap_usd = Column(Numeric(24, 2))
    total_volume_usd = Column(Numeric(24, 2))
    price_change_24h = Column(Numeric(12, 4))
    high_24h = Column(Numeric(24, 8))
    low_24h = Column(Numeric(24, 8))
    circulating_supply = Column(Numeric(24, 2))
    source = Column(String(50), default="coingecko")
    raw_response_id = Column(String(100))
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (
        UniqueConstraint("coin_id", "price_date", name="uq_crypto_daily_price"),
        Index("idx_crypto_price_date", "price_date"),
        Index("idx_crypto_price_coin", "coin_id"),
    )

    def to_dict(self):
        return {
            "coin_id": self.coin_id,
            "date": self.price_date.isoformat(),
            "price_usd": float(self.price_usd) if self.price_usd else None,
            "market_cap_usd": float(self.market_cap_usd) if self.market_cap_usd else None,
            "total_volume_usd": float(self.total_volume_usd) if self.total_volume_usd else None,
            "price_change_24h": float(self.price_change_24h) if self.price_change_24h else None,
        }
