# 🏦 MFAPIs — Financial Data API Platform

> Unified financial data ETL platform that acquires public financial data,
> normalizes it through modular pipelines, and serves it through
> standardized outputs and APIs.

## 🎯 Project Overview

MFAPIs expands from mutual fund data into a comprehensive financial data platform covering equities, forex, crypto, bonds, economic indicators, and technical analytics. The platform implements complete ETL pipelines for three categories with a modular architecture designed for extension to all ten data categories.

## 🏗️ Architecture

```
Public Data Sources → ETL Pipelines → PostgreSQL → Output/API
(Frankfurter, CoinGecko, FRED)   (Python)        (Normalized)    (JSON)
```

**ETL Flow per Category:**
```
Extract (API call + raw save) → Transform (clean + validate) → Load (upsert to DB + export JSON)
```

## ⚙️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.10+ | Core language |
| PostgreSQL 17+ | Relational database storage |
| SQLAlchemy 2.0 | ORM & database session management |
| Pandas | Tabular data transformation & normalization |
| Requests & Tenacity | HTTP data extraction with exponential backoff |
| pytest | Automated test suite with coverage reporting |
| structlog | Structured JSON logging |
| Pydantic | Configuration validation |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 17+ (running on `localhost:5432`)
- FRED API key (free: https://fred.stlouisfed.org/docs/api/api_key.html)

### Setup

```bash
# 1. Clone/Enter project
cd "backend assignment"

# 2. Create virtual environment
python -m venv venv

# Activate (choose your platform):
.\venv\Scripts\Activate.ps1          # Windows PowerShell
source venv/bin/activate              # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env                # Windows
cp .env.example .env                  # macOS / Linux
# Edit .env with your PostgreSQL credentials and FRED_API_KEY

# 5. Create database (run in psql or pgAdmin)
# CREATE DATABASE mfapis_db;

# 6. Initialize database tables
python -m scripts.init_db
```

### Running Pipelines

```bash
# Run individual pipelines
python -m pipelines.forex_pipeline       # ~20s, no API key needed
python -m pipelines.crypto_pipeline      # ~25s, no API key needed
python -m pipelines.economic_pipeline    # ~120s, requires FRED_API_KEY

# Run all pipelines sequentially
python -m pipelines.run_all
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with test coverage
python -m pytest tests/ -v --cov=. --cov-report=term-missing
```

## 📁 Project Structure

```
backend assignment/
├── config/               # Settings and structured logging setup
│   ├── settings.py       # Centralized configuration (DB, APIs, params)
│   └── logging_config.py # structlog JSON logging setup
├── models/               # SQLAlchemy ORM models
│   ├── forex.py          # ForexPair, ForexDailyRate
│   ├── crypto.py         # Cryptocurrency, CryptoDailyPrice
│   ├── economic.py       # EconomicIndicator, EconomicIndicatorValue
│   └── pipeline.py       # PipelineRun (execution tracking)
├── extractors/           # Modular data extractors with retry logic
│   ├── base_extractor.py # Abstract base with retry, raw save
│   ├── forex_extractor.py
│   ├── crypto_extractor.py
│   └── economic_extractor.py
├── transformers/         # Normalization and data cleaning
│   ├── base_transformer.py # Helpers: _safe_float, _safe_date
│   ├── forex_transformer.py
│   ├── crypto_transformer.py
│   └── economic_transformer.py
├── loaders/              # Database & export
│   ├── db_loader.py      # PostgreSQL UPSERT logic
│   └── json_exporter.py  # Standardized JSON output
├── pipelines/            # E→T→L orchestration scripts
│   ├── forex_pipeline.py
│   ├── crypto_pipeline.py
│   ├── economic_pipeline.py
│   └── run_all.py        # Run all pipelines with error isolation
├── tests/                # Automated test suite
│   ├── conftest.py       # Shared fixtures with realistic data
│   ├── test_transformers.py  # 15 transformer tests
│   ├── test_extractors.py    # 15 extractor tests
│   └── test_pipelines.py     # 10 integration tests
├── raw_responses/        # Preserved raw JSON from APIs
├── output/               # Standardized sample JSON outputs
├── docs/                 # Documentation
│   ├── source_catalogue.md
│   ├── commercial_strategy.md
│   ├── api_design.md
│   ├── data_quality.md
│   └── licensing.md
├── schemas/              # PostgreSQL DDL (create_tables.sql)
├── scripts/              # Utility scripts (init_db.py)
├── .env.example          # Environment variable template
├── requirements.txt      # Python dependencies
├── pyproject.toml        # pytest configuration
└── README.md
```

## 🔌 Implemented Pipelines

| Pipeline | Source API | Coverage | Records Loaded |
|----------|-----------|----------|----------------|
| **Forex** | Frankfurter (ECB) | 145 currency pairs, 1 year daily rates | ~3,700+ |
| **Crypto** | CoinGecko | Top 50 coins, 365-day price history | ~1,900+ |
| **Economic** | FRED | 8 US macro indicators (GDP, CPI, etc.) | ~29,000+ |

**Total: ~34,600+ records across 7 database tables**

## 🗄️ Database Schema

| Table | Description | Unique Constraint |
|-------|-------------|-------------------|
| `forex_pairs` | Currency pair definitions | `(base_currency, target_currency)` |
| `forex_daily_rates` | Daily exchange rates | `(base_currency, target_currency, rate_date)` |
| `cryptocurrencies` | Coin metadata | `(coin_id)` |
| `crypto_daily_prices` | Daily crypto prices | `(coin_id, price_date)` |
| `economic_indicators` | Indicator metadata | `(indicator_id)` |
| `economic_indicator_values` | Time series values | `(indicator_id, observation_date)` |
| `pipeline_runs` | ETL execution logs | — |

## 📊 Sample Standardized JSON Output

```json
{
  "status": "success",
  "meta": {
    "source": "frankfurter",
    "category": "forex",
    "total_records": 3591,
    "sample_size": 25,
    "generated_at": "2026-11-05T17:00:00+00:00"
  },
  "data": [
    {
      "base_currency": "USD",
      "target_currency": "INR",
      "rate_date": "2026-11-05",
      "exchange_rate": 84.125,
      "source": "frankfurter"
    }
  ]
}
```

## 📋 Documentation

| Document | Description |
|----------|-------------|
| [Source Catalogue](docs/source_catalogue.md) | 30+ public sources across all 10 financial data categories |
| [Commercial Strategy](docs/commercial_strategy.md) | Ranked opportunities, customer segments, pricing models, GTM plans |
| [API Design](docs/api_design.md) | REST API v1 endpoints with request/response examples |
| [Data Quality](docs/data_quality.md) | Validation pipeline, quality metrics, monitoring framework |
| [Licensing](docs/licensing.md) | Source licensing, attribution requirements, compliance checklist |
