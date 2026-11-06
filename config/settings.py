import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:1234567@localhost:5432/mfapis_db"
    )
    FRED_API_KEY: str = os.getenv("FRED_API_KEY", "")
    ALPHA_VANTAGE_API_KEY: str = os.getenv("ALPHA_VANTAGE_API_KEY", "")

    FRANKFURTER_BASE_URL: str = "https://api.frankfurter.app"
    COINGECKO_BASE_URL: str = "https://api.coingecko.com/api/v3"
    FRED_BASE_URL: str = "https://api.stlouisfed.org/fred"

    RAW_RESPONSES_DIR: Path = BASE_DIR / "raw_responses"
    OUTPUT_DIR: Path = BASE_DIR / "output"

    MAX_RETRIES: int = 3
    RETRY_DELAY_SECONDS: int = 5
    REQUEST_TIMEOUT: int = 30
    BATCH_SIZE: int = 1000

    FOREX_BASE_CURRENCIES: list = ["USD", "EUR", "GBP", "JPY", "INR"]
    FOREX_TARGET_CURRENCIES: list = ["USD", "EUR", "GBP", "JPY", "INR", "AUD", "CAD", "CHF"]

    CRYPTO_TOP_N: int = 50
    CRYPTO_VS_CURRENCY: str = "usd"

    ECONOMIC_INDICATORS: dict = {
        "GDP": {
            "name": "Gross Domestic Product",
            "category": "GDP",
            "frequency": "quarterly"
        },
        "CPIAUCSL": {
            "name": "Consumer Price Index (All Urban Consumers)",
            "category": "Inflation",
            "frequency": "monthly"
        },
        "UNRATE": {
            "name": "Unemployment Rate",
            "category": "Employment",
            "frequency": "monthly"
        },
        "FEDFUNDS": {
            "name": "Federal Funds Effective Rate",
            "category": "Interest Rates",
            "frequency": "monthly"
        },
        "DGS10": {
            "name": "10-Year Treasury Constant Maturity Rate",
            "category": "Bonds",
            "frequency": "daily"
        },
        "DEXUSEU": {
            "name": "US Dollar / Euro Exchange Rate",
            "category": "Exchange Rates",
            "frequency": "daily"
        },
        "INDPRO": {
            "name": "Industrial Production Index",
            "category": "Production",
            "frequency": "monthly"
        },
        "TOTALSA": {
            "name": "Total Vehicle Sales",
            "category": "Economic Activity",
            "frequency": "monthly"
        }
    }

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
