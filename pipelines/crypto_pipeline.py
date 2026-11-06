import sys, os, time
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.logging_config import setup_logging, get_logger
from extractors.crypto_extractor import CryptoExtractor
from transformers.crypto_transformer import CryptoTransformer
from loaders.db_loader import DatabaseLoader
from loaders.json_exporter import export_sample_json
from models.base import init_database

logger = get_logger("CryptoPipeline")


def run_crypto_pipeline():
    start_time = time.time()
    started_at = datetime.now(timezone.utc)
    loader = DatabaseLoader()

    logger.info("=" * 60)
    logger.info("CRYPTO PIPELINE STARTED")
    logger.info("=" * 60)

    try:
        logger.info("Step 1: EXTRACT — Fetching data from CoinGecko API...")
        extractor = CryptoExtractor()
        raw_data = extractor.extract()
        logger.info("Extraction complete")

        logger.info("Step 2: TRANSFORM — Cleaning and normalizing data...")
        transformer = CryptoTransformer()
        transformed = transformer.transform(raw_data)
        coins_df = transformed["coins"]
        prices_df = transformed["daily_prices"]
        logger.info(
            "Transformation complete",
            coins=len(coins_df),
            prices=len(prices_df)
        )

        logger.info("Step 3: LOAD — Inserting into PostgreSQL...")
        coins_loaded = loader.load_crypto_coins(coins_df)
        prices_loaded = loader.load_crypto_prices(prices_df)
        logger.info(
            "Loading complete",
            coins_loaded=coins_loaded,
            prices_loaded=prices_loaded
        )

        logger.info("Step 4: EXPORT — Generating sample JSON...")
        if not prices_df.empty:
            export_sample_json(
                prices_df, "crypto_sample.json", sample_size=25,
                metadata={"source": "coingecko", "category": "cryptocurrency"}
            )

        duration = round(time.time() - start_time, 2)

        loader.log_pipeline_run(
            pipeline_name="crypto",
            status="success",
            records_extracted=len(raw_data.get("market_data", [])),
            records_transformed=len(prices_df),
            records_loaded=coins_loaded + prices_loaded,
            started_at=started_at,
            duration_seconds=duration
        )

        logger.info("=" * 60)
        logger.info(f"CRYPTO PIPELINE COMPLETED in {duration}s",
                    coins=coins_loaded, prices=prices_loaded)
        logger.info("=" * 60)
        return {"status": "success", "coins": coins_loaded, "prices": prices_loaded}

    except Exception as e:
        duration = round(time.time() - start_time, 2)
        loader.log_pipeline_run(
            pipeline_name="crypto",
            status="failed",
            error_message=str(e),
            started_at=started_at,
            duration_seconds=duration
        )
        logger.error(f"CRYPTO PIPELINE FAILED: {e}")
        raise

if __name__ == "__main__":
    setup_logging()
    init_database()
    run_crypto_pipeline()
