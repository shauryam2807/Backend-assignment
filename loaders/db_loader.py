from typing import List, Dict
from datetime import datetime, timezone

import pandas as pd
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert as pg_insert

from models.base import engine, get_session
from models.forex import ForexPair, ForexDailyRate
from models.crypto import Cryptocurrency, CryptoDailyPrice
from models.economic import EconomicIndicator, EconomicIndicatorValue
from models.pipeline import PipelineRun
from config.logging_config import get_logger

logger = get_logger("db_loader")


def _utcnow():
    return datetime.now(timezone.utc)


class DatabaseLoader:

    def __init__(self):
        self.logger = get_logger("DatabaseLoader")

    def load_forex_pairs(self, df: pd.DataFrame) -> int:
        if df.empty:
            self.logger.warning("No forex pairs to load")
            return 0

        records = df.to_dict(orient="records")
        loaded = 0

        with get_session() as session:
            for record in records:
                stmt = pg_insert(ForexPair).values(
                    base_currency=record["base_currency"],
                    target_currency=record["target_currency"],
                    pair_name=record["pair_name"],
                    source=record.get("source", "frankfurter"),
                    is_active=record.get("is_active", True),
                    updated_at=_utcnow()
                )

                stmt = stmt.on_conflict_do_update(
                    constraint="uq_forex_pair",
                    set_={
                        "pair_name": stmt.excluded.pair_name,
                        "is_active": stmt.excluded.is_active,
                        "updated_at": _utcnow()
                    }
                )

                session.execute(stmt)
                loaded += 1

        self.logger.info("Forex pairs loaded", count=loaded)
        return loaded

    def load_forex_rates(self, df: pd.DataFrame) -> int:
        if df.empty:
            self.logger.warning("No forex rates to load")
            return 0

        records = df.to_dict(orient="records")
        loaded = 0
        batch_size = 500

        with get_session() as session:
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]

                for record in batch:
                    stmt = pg_insert(ForexDailyRate).values(
                        base_currency=record["base_currency"],
                        target_currency=record["target_currency"],
                        rate_date=record["rate_date"],
                        exchange_rate=record["exchange_rate"],
                        source=record.get("source", "frankfurter"),
                        raw_response_id=record.get("raw_response_id"),
                        updated_at=_utcnow()
                    )

                    stmt = stmt.on_conflict_do_update(
                        constraint="uq_forex_daily_rate",
                        set_={
                            "exchange_rate": stmt.excluded.exchange_rate,
                            "updated_at": _utcnow()
                        }
                    )

                    session.execute(stmt)
                    loaded += 1

                self.logger.info(f"Batch loaded: {min(i + batch_size, len(records))}/{len(records)}")

        self.logger.info("Forex rates loaded", count=loaded)
        return loaded

    def load_crypto_coins(self, df: pd.DataFrame) -> int:
        if df.empty:
            return 0

        records = df.to_dict(orient="records")
        loaded = 0

        with get_session() as session:
            for record in records:
                stmt = pg_insert(Cryptocurrency).values(
                    coin_id=record["coin_id"],
                    symbol=record["symbol"],
                    name=record["name"],
                    market_cap_rank=record.get("market_cap_rank"),
                    category=record.get("category"),
                    image_url=record.get("image_url"),
                    source="coingecko",
                    is_active=True,
                    updated_at=_utcnow()
                )

                stmt = stmt.on_conflict_do_update(
                    index_elements=["coin_id"],
                    set_={
                        "symbol": stmt.excluded.symbol,
                        "name": stmt.excluded.name,
                        "market_cap_rank": stmt.excluded.market_cap_rank,
                        "image_url": stmt.excluded.image_url,
                        "updated_at": _utcnow()
                    }
                )

                session.execute(stmt)
                loaded += 1

        self.logger.info("Crypto coins loaded", count=loaded)
        return loaded

    def load_crypto_prices(self, df: pd.DataFrame) -> int:
        if df.empty:
            return 0

        records = df.to_dict(orient="records")
        loaded = 0

        with get_session() as session:
            for i in range(0, len(records), 500):
                batch = records[i:i + 500]

                for record in batch:
                    stmt = pg_insert(CryptoDailyPrice).values(
                        coin_id=record["coin_id"],
                        price_date=record["price_date"],
                        price_usd=record.get("price_usd"),
                        market_cap_usd=record.get("market_cap_usd"),
                        total_volume_usd=record.get("total_volume_usd"),
                        price_change_24h=record.get("price_change_24h"),
                        high_24h=record.get("high_24h"),
                        low_24h=record.get("low_24h"),
                        circulating_supply=record.get("circulating_supply"),
                        source="coingecko",
                        raw_response_id=record.get("raw_response_id"),
                        updated_at=_utcnow()
                    )

                    stmt = stmt.on_conflict_do_update(
                        constraint="uq_crypto_daily_price",
                        set_={
                            "price_usd": stmt.excluded.price_usd,
                            "market_cap_usd": stmt.excluded.market_cap_usd,
                            "total_volume_usd": stmt.excluded.total_volume_usd,
                            "updated_at": _utcnow()
                        }
                    )

                    session.execute(stmt)
                    loaded += 1

        self.logger.info("Crypto prices loaded", count=loaded)
        return loaded

    def load_economic_indicators(self, df: pd.DataFrame) -> int:
        if df.empty:
            return 0

        records = df.to_dict(orient="records")
        loaded = 0

        with get_session() as session:
            for record in records:
                stmt = pg_insert(EconomicIndicator).values(
                    indicator_id=record["indicator_id"],
                    name=record["name"],
                    description=record.get("description"),
                    frequency=record.get("frequency"),
                    units=record.get("units"),
                    seasonal_adjustment=record.get("seasonal_adjustment"),
                    country=record.get("country", "US"),
                    category=record.get("category"),
                    source_agency=record.get("source_agency"),
                    source="fred",
                    is_active=True,
                    updated_at=_utcnow()
                )

                stmt = stmt.on_conflict_do_update(
                    index_elements=["indicator_id"],
                    set_={
                        "name": stmt.excluded.name,
                        "description": stmt.excluded.description,
                        "frequency": stmt.excluded.frequency,
                        "units": stmt.excluded.units,
                        "updated_at": _utcnow()
                    }
                )

                session.execute(stmt)
                loaded += 1

        self.logger.info("Economic indicators loaded", count=loaded)
        return loaded

    def load_economic_values(self, df: pd.DataFrame) -> int:
        if df.empty:
            return 0

        records = df.to_dict(orient="records")
        loaded = 0

        with get_session() as session:
            for i in range(0, len(records), 500):
                batch = records[i:i + 500]

                for record in batch:
                    stmt = pg_insert(EconomicIndicatorValue).values(
                        indicator_id=record["indicator_id"],
                        observation_date=record["observation_date"],
                        value=record.get("value"),
                        country=record.get("country", "US"),
                        source="fred",
                        raw_response_id=record.get("raw_response_id"),
                        updated_at=_utcnow()
                    )

                    stmt = stmt.on_conflict_do_update(
                        constraint="uq_economic_value",
                        set_={
                            "value": stmt.excluded.value,
                            "updated_at": _utcnow()
                        }
                    )

                    session.execute(stmt)
                    loaded += 1

        self.logger.info("Economic values loaded", count=loaded)
        return loaded

    def log_pipeline_run(
        self,
        pipeline_name: str,
        status: str,
        records_extracted: int = 0,
        records_transformed: int = 0,
        records_loaded: int = 0,
        error_message: str = None,
        started_at: datetime = None,
        duration_seconds: float = None
    ):
        with get_session() as session:
            run = PipelineRun(
                pipeline_name=pipeline_name,
                run_status=status,
                records_extracted=records_extracted,
                records_transformed=records_transformed,
                records_loaded=records_loaded,
                error_message=error_message,
                started_at=started_at or _utcnow(),
                completed_at=_utcnow(),
                duration_seconds=duration_seconds
            )
            session.add(run)

        self.logger.info(
            "Pipeline run logged",
            pipeline=pipeline_name,
            status=status,
            loaded=records_loaded
        )
