# 🏦 MFAPIs — Financial Data API Platform

> Unified financial data ETL platform that acquires public financial data,
> normalizes it through modular pipelines, and serves it through
> standardized outputs and APIs — **Twelve Data compatible**.

## 🎯 Project Overview

MFAPIs expands from mutual fund data into a comprehensive financial data platform covering equities, forex, crypto, bonds, economic indicators, and technical analytics. The platform implements complete ETL pipelines for three categories with a modular architecture designed for extension to all ten data categories.

**Key Achievement:** Crypto and Forex OHLCV data matches Twelve Data's output format and quality with < 0.1% variance (verified against live Twelve Data API).

## 🏗️ Architecture

```
Public Data Sources → ETL Pipelines → PostgreSQL → Output/API
(Binance, Yahoo Finance,   (Python)      (Normalized)    (JSON + REST)
 Frankfurter, CoinGecko,
 FRED)
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
| pytest | Automated test suite (79 tests) |
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
python -m pipelines.forex_pipeline          # ~20s, no API key needed
python -m pipelines.crypto_pipeline         # ~25s, no API key needed
python -m pipelines.economic_pipeline       # ~120s, requires FRED_API_KEY
python -m pipelines.crypto_ohlcv_pipeline   # ~15s, Binance OHLCV (no key)
python -m pipelines.forex_ohlc_pipeline     # ~10s, Yahoo Finance OHLC (no key)

# Run all pipelines sequentially
python -m pipelines.run_all
```

### Starting the API Server

```bash
python server.py
# Server runs at http://localhost:10000
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
├── config/                        # Settings and structured logging setup
│   ├── settings.py                # Centralized config (DB, APIs, Binance, Yahoo Finance)
│   └── logging_config.py          # structlog JSON logging setup
├── models/                        # SQLAlchemy ORM models
│   ├── forex.py                   # ForexPair, ForexDailyRate, ForexOHLCV
│   ├── crypto.py                  # Cryptocurrency, CryptoDailyPrice, CryptoOHLCV
│   ├── economic.py                # EconomicIndicator, EconomicIndicatorValue
│   └── pipeline.py                # PipelineRun (execution tracking)
├── extractors/                    # Modular data extractors with retry logic
│   ├── base_extractor.py          # Abstract base with retry, raw save
│   ├── forex_extractor.py         # Frankfurter API (ECB rates)
│   ├── crypto_extractor.py        # CoinGecko API (market data)
│   ├── economic_extractor.py      # FRED API (macro indicators)
│   ├── binance_extractor.py       # Binance Public API (crypto OHLCV klines)
│   └── forex_ohlc_extractor.py    # Yahoo Finance (forex OHLC candles)
├── transformers/                  # Normalization and data cleaning
│   ├── base_transformer.py        # Helpers: _safe_float, _safe_date, validation
│   ├── forex_transformer.py       # ECB rate normalization
│   ├── crypto_transformer.py      # CoinGecko data normalization
│   ├── economic_transformer.py    # FRED series normalization
│   ├── binance_transformer.py     # Binance klines → OHLCV DataFrame
│   └── forex_ohlc_transformer.py  # Yahoo Finance chart → OHLCV DataFrame
├── loaders/                       # Database & export
│   ├── db_loader.py               # PostgreSQL UPSERT logic (all tables)
│   └── json_exporter.py           # Standardized JSON output
├── pipelines/                     # E→T→L orchestration scripts
│   ├── forex_pipeline.py          # ECB forex rates pipeline
│   ├── crypto_pipeline.py         # CoinGecko market data pipeline
│   ├── economic_pipeline.py       # FRED macro indicators pipeline
│   ├── crypto_ohlcv_pipeline.py   # Binance OHLCV pipeline (Twelve Data match)
│   ├── forex_ohlc_pipeline.py     # Yahoo Finance OHLC pipeline (Twelve Data match)
│   └── run_all.py                 # Run all 5 pipelines with error isolation
├── services/                      # Real-time data fetching & caching layer
│   ├── cache.py                   # Thread-safe TTL cache (30s default)
│   └── live_fetcher.py            # Live feeds: Binance (crypto) + Yahoo Finance (forex)
├── tests/                         # Automated test suite (79 tests)
│   ├── conftest.py                # Shared fixtures with realistic data
│   ├── test_transformers.py       # 15 transformer tests
│   ├── test_extractors.py         # 15 extractor tests
│   ├── test_pipelines.py          # 10 integration tests
│   ├── test_services.py           # 25 services layer tests (cache + live fetcher)
│   └── test_twelvedata_parity.py  # 6 Twelve Data parity tests (Binance + Yahoo)
├── scripts/                       # Utility scripts
│   ├── init_db.py                 # Database table initialization
│   └── verify_against_twelvedata.py  # Live parity verification vs Twelve Data API
├── raw_responses/                 # Preserved raw JSON from APIs
├── output/                        # Standardized sample JSON outputs
├── docs/                          # Documentation
│   ├── source_catalogue.md        # 30+ public sources across all categories
│   ├── commercial_strategy.md     # Ranked opportunities, pricing, GTM plans
│   ├── api_design.md              # REST API endpoints with examples
│   ├── data_quality.md            # Validation pipeline, quality metrics
│   └── licensing.md               # Source licensing, compliance checklist
├── schemas/                       # PostgreSQL DDL (create_tables.sql)
├── server.py                      # HTTP server with Twelve Data compatible API
├── .env.example                   # Environment variable template
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # pytest configuration
└── README.md
```

## 🔌 Implemented Pipelines

| Pipeline | Source API | Coverage | Records Loaded |
|----------|-----------|----------|----------------|
| **Forex Rates** | Frankfurter (ECB) | 145 currency pairs, 1 year daily rates | ~3,700+ |
| **Crypto Market** | CoinGecko | Top 50 coins, 365-day price history | ~1,900+ |
| **Economic** | FRED | 8 US macro indicators (GDP, CPI, etc.) | ~29,000+ |
| **Crypto OHLCV** | Binance Public API | 5 symbols (BTC, ETH, SOL, BNB, XRP), 365 daily candles | ~1,825 |
| **Forex OHLC** | Yahoo Finance | 7 pairs (EUR/USD, GBP/USD, etc.), ~260 trading days | ~1,813 |

**Total: ~38,200+ records across 9 database tables**

## 🗄️ Database Schema

| Table | Description | Unique Constraint |
|-------|-------------|-------------------|
| `forex_pairs` | Currency pair definitions | `(base_currency, target_currency)` |
| `forex_daily_rates` | Daily exchange rates | `(base_currency, target_currency, rate_date)` |
| `forex_ohlcv_daily` | Forex OHLCV candles (Yahoo Finance) | `(pair_name, candle_date)` |
| `cryptocurrencies` | Coin metadata | `(coin_id)` |
| `crypto_daily_prices` | Daily crypto prices | `(coin_id, price_date)` |
| `crypto_ohlcv_daily` | Crypto OHLCV candles (Binance) | `(symbol, candle_date)` |
| `economic_indicators` | Indicator metadata | `(indicator_id)` |
| `economic_indicator_values` | Time series values | `(indicator_id, observation_date)` |
| `pipeline_runs` | ETL execution logs | — |

## 🔗 Twelve Data Compatible API Endpoints

The server provides Twelve Data compatible endpoints serving real OHLCV data:

| Endpoint | Description | Example |
|----------|-------------|---------|
| `/time_series` | OHLCV candle data | `?symbol=BTC/USD&interval=1day&outputsize=30` |
| `/quote` | Real-time quote snapshot | `?symbol=BTC/USD` |
| `/price` | Latest close price | `?symbol=ETH/USD` |
| `/exchange_rate` | Currency exchange rate | `?symbol=EUR/USD` |
| `/eod` | End-of-day price | `?symbol=BTC/USD` |
| `/cryptocurrencies` | Available crypto symbols | — |
| `/forex_pairs` | Available forex pairs | — |

**Response Format (matches Twelve Data exactly):**
```json
{
  "meta": {
    "symbol": "BTC/USD",
    "interval": "1day",
    "currency_base": "BTC",
    "currency_quote": "USD",
    "exchange": "Binance",
    "type": "Digital Currency"
  },
  "values": [
    {
      "datetime": "2026-11-09",
      "open": "76450.00",
      "high": "77200.00",
      "low": "75800.00",
      "close": "76900.00",
      "volume": "12345"
    }
  ],
  "status": "ok"
}
```

## 📊 Data Quality & Parity

| Data Source | vs Twelve Data | Variance |
|-------------|---------------|----------|
| **Crypto OHLCV (Binance)** | Open/High/Low: 0.000% | ✅ Exact Match |
| **Crypto Close** | < 0.06% (live candle timing) | ✅ Pass |
| **Forex OHLCV (Yahoo Finance)** | < 0.03% | ✅ Pass |

Verified using `scripts/verify_against_twelvedata.py` against live Twelve Data API.

## 📋 Documentation

| Document | Description |
|----------|-------------|
| [Source Catalogue](docs/source_catalogue.md) | 30+ public sources across all 10 financial data categories |
| [Commercial Strategy](docs/commercial_strategy.md) | Ranked opportunities, customer segments, pricing models, GTM plans |
| [API Design](docs/api_design.md) | REST API endpoints with request/response examples |
| [Data Quality](docs/data_quality.md) | Validation pipeline, quality metrics, monitoring framework |
| [Licensing](docs/licensing.md) | Source licensing, attribution requirements, compliance checklist |
