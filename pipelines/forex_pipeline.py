import sys
import os
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.logging_config import setup_logging, get_logger
from extractors.forex_extractor import ForexExtractor
from transformers.forex_transformer import ForexTransformer
from loaders.db_loader import DatabaseLoader
from loaders.json_exporter import export_sample_json
from models.base import init_database

logger = get_logger("ForexPipeline")


def run_forex_pipeline():
    start_time = time.time()
    started_at = datetime.now(timezone.utc)
    loader = DatabaseLoader()

    logger.info("=" * 60)
    logger.info("FOREX PIPELINE STARTED")
    logger.info("=" * 60)

    try:
        logger.info("Step 1: EXTRACT — Fetching data from Frankfurter API...")
        extractor = ForexExtractor()
        raw_data = extractor.extract()
        logger.info("Extraction complete")

        logger.info("Step 2: TRANSFORM — Cleaning and normalizing data...")
        transformer = ForexTransformer()
        transformed = transformer.transform(raw_data)
        pairs_df = transformed["pairs"]
        rates_df = transformed["daily_rates"]
        logger.info(
            "Transformation complete",
            pairs=len(pairs_df),
            rates=len(rates_df)
        )

        logger.info("Step 3: LOAD — Inserting into PostgreSQL...")
        pairs_loaded = loader.load_forex_pairs(pairs_df)
        rates_loaded = loader.load_forex_rates(rates_df)
        logger.info(
            "Loading complete",
            pairs_loaded=pairs_loaded,
            rates_loaded=rates_loaded
        )

        logger.info("Step 4: EXPORT — Generating sample JSON...")
        if not rates_df.empty:
            export_sample_json(
                rates_df,
                "forex_sample.json",
                sample_size=25,
                metadata={
                    "source": "frankfurter",
                    "category": "forex",
                    "description": "Daily exchange rates from ECB via Frankfurter API"
                }
            )

        duration = round(time.time() - start_time, 2)

        loader.log_pipeline_run(
            pipeline_name="forex",
            status="success",
            records_extracted=len(raw_data.get("historical_rates", [])),
            records_transformed=len(rates_df),
            records_loaded=pairs_loaded + rates_loaded,
            started_at=started_at,
            duration_seconds=duration
        )

        logger.info("=" * 60)
        logger.info(
            f"FOREX PIPELINE COMPLETED in {duration}s",
            pairs_loaded=pairs_loaded,
            rates_loaded=rates_loaded,
            duration_seconds=duration
        )
        logger.info("=" * 60)

        return {"status": "success", "pairs": pairs_loaded, "rates": rates_loaded}

    except Exception as e:
        duration = round(time.time() - start_time, 2)
        loader.log_pipeline_run(
            pipeline_name="forex",
            status="failed",
            error_message=str(e),
            started_at=started_at,
            duration_seconds=duration
        )
        logger.error(
            f"FOREX PIPELINE FAILED after {duration}s",
            error=str(e)
        )
        raise


if __name__ == "__main__":
    setup_logging()
    init_database()
    run_forex_pipeline()
