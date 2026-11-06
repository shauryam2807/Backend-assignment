import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.logging_config import setup_logging, get_logger
from models.base import init_database

logger = get_logger("init_db")

if __name__ == "__main__":
    setup_logging()
    print("=" * 50)
    print("MFAPIs Database Initialization")
    print("=" * 50)
    print("Creating tables in PostgreSQL...")
    try:
        init_database()
        print("All database tables created successfully!")
        print("Tables: forex_pairs, forex_daily_rates,")
        print("        cryptocurrencies, crypto_daily_prices,")
        print("        economic_indicators, economic_indicator_values,")
        print("        pipeline_runs")
        print("=" * 50)
    except Exception as e:
        print(f"ERROR: {e}")
        print("Check your DATABASE_URL in .env file")
        sys.exit(1)
