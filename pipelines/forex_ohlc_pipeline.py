import sys
import os
import time
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config.logging_config import setup_logging, get_logger
from extractors.forex_ohlc_extractor import ForexOHLCExtractor
from transformers.forex_ohlc_transformer import ForexOHLCTransformer
from loaders.db_loader import DatabaseLoader
from loaders.json_exporter import export_sample_json
from models.base import init_database

logger = get_logger("ForexOHLCPipeline")


def run_forex_ohlc_pipeline():
    start_time = time.time()
    started_at = datetime.now(timezone.utc)
    loader = DatabaseLoader()

    logger.info("=" * 60)
    logger.info("FOREX OHLC PIPELINE STARTED (Institutional Chart Feeds)")
    logger.info("=" * 60)

    try:
        logger.info("Step 1: EXTRACT — Fetching institutional Forex OHLC charts...")
        extractor = ForexOHLCExtractor()
        raw_data = extractor.extract(range_days="1y")
        logger.info("Extraction complete", pairs=len(raw_data))

        logger.info("Step 2: TRANSFORM — Parsing real Forex OHLC candles...")
        transformer = ForexOHLCTransformer()
        ohlc_df = transformer.transform(raw_data)
        logger.info("Transformation complete", candles=len(ohlc_df))

        logger.info("Step 3: LOAD — Inserting Forex OHLC into PostgreSQL...")
        candles_loaded = loader.load_forex_ohlcv(ohlc_df)
        logger.info("Database loading complete", candles_loaded=candles_loaded)

        logger.info("Step 4: EXPORT — Generating standard Twelve Data format JSON sample...")
        if not ohlc_df.empty:
            export_sample_json(
                ohlc_df,
                "forex_ohlcv_sample.json",
                sample_size=100,
                metadata={"source": "yahoo_finance", "asset_type": "forex_ohlcv", "standard": "twelvedata_compatible"}
            )

        duration = round(time.time() - start_time, 2)
        loader.log_pipeline_run(
            pipeline_name="forex_ohlc",
            status="success",
            records_extracted=len(raw_data),
            records_transformed=len(ohlc_df),
            records_loaded=candles_loaded,
            started_at=started_at,
            duration_seconds=duration
        )

        logger.info("=" * 60)
        logger.info(f"FOREX OHLC PIPELINE COMPLETED in {duration}s", candles=candles_loaded)
        logger.info("=" * 60)
        return {"status": "success", "candles": candles_loaded}

    except Exception as e:
        duration = round(time.time() - start_time, 2)
        loader.log_pipeline_run(
            pipeline_name="forex_ohlc",
            status="failed",
            error_message=str(e),
            started_at=started_at,
            duration_seconds=duration
        )
        logger.error(f"FOREX OHLC PIPELINE FAILED: {e}")
        raise


if __name__ == "__main__":
    setup_logging()
    init_database()
    run_forex_ohlc_pipeline()

