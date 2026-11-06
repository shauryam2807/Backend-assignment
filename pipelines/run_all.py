import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.logging_config import setup_logging, get_logger
from models.base import init_database
from pipelines.forex_pipeline import run_forex_pipeline
from pipelines.crypto_pipeline import run_crypto_pipeline
from pipelines.economic_pipeline import run_economic_pipeline

logger = get_logger("RunAllPipelines")


def run_all():
    setup_logging()
    init_database()

    start = time.time()
    results = {}

    logger.info("=" * 60)
    logger.info("RUNNING ALL ETL PIPELINES")
    logger.info("=" * 60)

    try:
        results["forex"] = run_forex_pipeline()
    except Exception as e:
        results["forex"] = {"status": "failed", "error": str(e)}
        logger.error(f"Forex pipeline failed: {e}")

    try:
        results["crypto"] = run_crypto_pipeline()
    except Exception as e:
        results["crypto"] = {"status": "failed", "error": str(e)}
        logger.error(f"Crypto pipeline failed: {e}")

    try:
        results["economic"] = run_economic_pipeline()
    except Exception as e:
        results["economic"] = {"status": "failed", "error": str(e)}
        logger.error(f"Economic pipeline failed: {e}")

    duration = round(time.time() - start, 2)
    logger.info("=" * 60)
    logger.info(f"ALL PIPELINES COMPLETED in {duration}s")
    for name, result in results.items():
        status = "SUCCESS" if result.get("status") == "success" else "FAILED"
        logger.info(f"  {status} {name}: {result}")
    logger.info("=" * 60)

    return results


if __name__ == "__main__":
    run_all()
