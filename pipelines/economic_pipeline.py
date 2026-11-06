import sys, os, time
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.logging_config import setup_logging, get_logger
from extractors.economic_extractor import EconomicExtractor
from transformers.economic_transformer import EconomicTransformer
from loaders.db_loader import DatabaseLoader
from loaders.json_exporter import export_sample_json
from models.base import init_database

logger = get_logger("EconomicPipeline")


def run_economic_pipeline():
    start_time = time.time()
    started_at = datetime.now(timezone.utc)
    loader = DatabaseLoader()

    logger.info("=" * 60)
    logger.info("ECONOMIC PIPELINE STARTED")
    logger.info("=" * 60)

    try:
        logger.info("Step 1: EXTRACT — Fetching data from FRED API...")
        extractor = EconomicExtractor()
        raw_data = extractor.extract()
        logger.info("Extraction complete")

        logger.info("Step 2: TRANSFORM — Cleaning and normalizing data...")
        transformer = EconomicTransformer()
        transformed = transformer.transform(raw_data)
        indicators_df = transformed["indicators"]
        values_df = transformed["values"]
        logger.info(
            "Transformation complete",
            indicators=len(indicators_df),
            values=len(values_df)
        )

        logger.info("Step 3: LOAD — Inserting into PostgreSQL...")
        ind_loaded = loader.load_economic_indicators(indicators_df)
        val_loaded = loader.load_economic_values(values_df)
        logger.info(
            "Loading complete",
            indicators_loaded=ind_loaded,
            values_loaded=val_loaded
        )

        logger.info("Step 4: EXPORT — Generating sample JSON...")
        if not values_df.empty:
            export_sample_json(
                values_df, "economic_sample.json", sample_size=30,
                metadata={"source": "fred", "category": "economic_indicators"}
            )

        duration = round(time.time() - start_time, 2)

        loader.log_pipeline_run(
            pipeline_name="economic",
            status="success",
            records_extracted=len(raw_data),
            records_transformed=len(values_df),
            records_loaded=ind_loaded + val_loaded,
            started_at=started_at,
            duration_seconds=duration
        )

        logger.info("=" * 60)
        logger.info(f"ECONOMIC PIPELINE COMPLETED in {duration}s",
                    indicators=ind_loaded, values=val_loaded)
        logger.info("=" * 60)
        return {"status": "success", "indicators": ind_loaded, "values": val_loaded}

    except Exception as e:
        duration = round(time.time() - start_time, 2)
        loader.log_pipeline_run(
            pipeline_name="economic",
            status="failed",
            error_message=str(e),
            started_at=started_at,
            duration_seconds=duration
        )
        logger.error(f"ECONOMIC PIPELINE FAILED: {e}")
        raise

if __name__ == "__main__":
    setup_logging()
    init_database()
    run_economic_pipeline()
