import pytest
import pandas as pd
from datetime import date, datetime


@pytest.fixture
def sample_forex_raw_data():
    return {
        "currencies": {
            "USD": "United States Dollar",
            "EUR": "Euro",
            "GBP": "British Pound",
            "INR": "Indian Rupee",
            "JPY": "Japanese Yen"
        },
        "latest_rates": {
            "USD": {
                "amount": 1,
                "base": "USD",
                "date": "2026-10-30",
                "rates": {
                    "EUR": 0.9215,
                    "GBP": 0.7921,
                    "INR": 84.50,
                    "JPY": 149.85
                }
            }
        },
        "historical_rates": [
            {
                "_base_currency": "USD",
                "_raw_id": "test_raw_001",
                "rates": {
                    "2026-10-28": {"EUR": 0.9210, "INR": 84.45},
                    "2026-10-29": {"EUR": 0.9212, "INR": 84.48},
                    "2026-10-30": {"EUR": 0.9215, "INR": 84.50}
                }
            }
        ]
    }


@pytest.fixture
def sample_crypto_raw_data():
    return {
        "market_data": [
            {
                "id": "bitcoin",
                "symbol": "btc",
                "name": "Bitcoin",
                "current_price": 67500.50,
                "market_cap": 1320000000000,
                "total_volume": 28000000000,
                "high_24h": 68000,
                "low_24h": 66800,
                "price_change_percentage_24h": 1.53,
                "market_cap_rank": 1,
                "circulating_supply": 19500000,
                "image": "https://example.com/btc.png"
            },
            {
                "id": "ethereum",
                "symbol": "eth",
                "name": "Ethereum",
                "current_price": 3450.25,
                "market_cap": 415000000000,
                "total_volume": 15000000000,
                "high_24h": 3500,
                "low_24h": 3400,
                "price_change_percentage_24h": -0.85,
                "market_cap_rank": 2,
                "circulating_supply": 120000000,
                "image": "https://example.com/eth.png"
            }
        ],
        "historical_data": {
            "bitcoin": {
                "prices": [
                    [1704067200000, 42000.50],
                    [1704153600000, 43100.20],
                    [1704240000000, 42500.75]
                ],
                "market_caps": [
                    [1704067200000, 820000000000],
                    [1704153600000, 842000000000],
                    [1704240000000, 830000000000]
                ],
                "total_volumes": [
                    [1704067200000, 15000000000],
                    [1704153600000, 18000000000],
                    [1704240000000, 16000000000]
                ],
                "_raw_id": "test_crypto_raw_001"
            }
        }
    }


@pytest.fixture
def sample_economic_raw_data():
    return {
        "GDP": {
            "metadata": {
                "seriess": [{
                    "id": "GDP",
                    "title": "Gross Domestic Product",
                    "frequency": "Quarterly",
                    "units": "Billions of Dollars",
                    "seasonal_adjustment": "Seasonally Adjusted Annual Rate",
                    "notes": "GDP data from BEA"
                }]
            },
            "observations": {
                "observations": [
                    {"date": "2024-01-01", "value": "27956.0"},
                    {"date": "2024-04-01", "value": "28276.4"},
                    {"date": "2024-07-01", "value": "28639.0"},
                    {"date": "2024-10-01", "value": "."}
                ],
                "_raw_id": "test_econ_raw_001"
            },
            "config": {
                "name": "Gross Domestic Product",
                "category": "GDP",
                "frequency": "quarterly"
            }
        }
    }


@pytest.fixture
def sample_forex_dataframe():
    return pd.DataFrame([
        {
            "base_currency": "USD",
            "target_currency": "INR",
            "rate_date": date(2026, 10, 30),
            "exchange_rate": 84.50,
            "source": "frankfurter",
            "raw_response_id": "test_001"
        },
        {
            "base_currency": "USD",
            "target_currency": "EUR",
            "rate_date": date(2026, 10, 30),
            "exchange_rate": 0.9215,
            "source": "frankfurter",
            "raw_response_id": "test_001"
        }
    ])
