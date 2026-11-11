import sys
import os
import time
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config.logging_config import setup_logging, get_logger
from extractors.binance_extractor import BinanceExtractor
from transformers.binance_transformer import BinanceTransformer
from loaders.db_loader import DatabaseLoader
from loaders.json_exporter import export_sample_json
from models.base import init_database

logger = get_logger("CryptoOHLCVPipeline")


def run_crypto_ohlcv_pipeline():
    start_time = time.time()
    started_at = datetime.now(timezone.utc)
    loader = DatabaseLoader()

    logger.info("=" * 60)
    logger.info("CRYPTO OHLCV PIPELINE STARTED (Binance/TwelveData Match)")
    logger.info("=" * 60)

    try:
        logger.info("Step 1: EXTRACT — Fetching klines from Binance Public API...")
        extractor = BinanceExtractor()
        raw_data = extractor.extract(limit=365)
        logger.info("Extraction complete", symbols=len(raw_data))

        logger.info("Step 2: TRANSFORM — Parsing real OHLCV candles...")
        transformer = BinanceTransformer()
        ohlcv_df = transformer.transform(raw_data)
        logger.info("Transformation complete", candles=len(ohlcv_df))

        logger.info("Step 3: LOAD — Inserting OHLCV candles into PostgreSQL...")
        candles_loaded = loader.load_crypto_ohlcv(ohlcv_df)
        logger.info("Database loading complete", candles_loaded=candles_loaded)

        logger.info("Step 4: EXPORT — Generating standard Twelve Data format JSON sample...")
        if not ohlcv_df.empty:
            export_sample_json(
                ohlcv_df,
                "crypto_ohlcv_sample.json",
                sample_size=100,
                metadata={"source": "binance", "asset_type": "crypto_ohlcv", "standard": "twelvedata_compatible"}
            )

        duration = round(time.time() - start_time, 2)
        loader.log_pipeline_run(
            pipeline_name="crypto_ohlcv",
            status="success",
            records_extracted=len(raw_data),
            records_transformed=len(ohlcv_df),
            records_loaded=candles_loaded,
            started_at=started_at,
            duration_seconds=duration
        )

        logger.info("=" * 60)
        logger.info(f"CRYPTO OHLCV PIPELINE COMPLETED in {duration}s", candles=candles_loaded)
        logger.info("=" * 60)
        return {"status": "success", "candles": candles_loaded}

    except Exception as e:
        duration = round(time.time() - start_time, 2)
        loader.log_pipeline_run(
            pipeline_name="crypto_ohlcv",
            status="failed",
            error_message=str(e),
            started_at=started_at,
            duration_seconds=duration
        )
        logger.error(f"CRYPTO OHLCV PIPELINE FAILED: {e}")
        raise


if __name__ == "__main__":
    setup_logging()
    init_database()
    run_crypto_ohlcv_pipeline()

