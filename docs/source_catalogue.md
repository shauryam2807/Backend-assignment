# 📋 MFAPIs Data Source Catalogue
> Complete inventory of public data sources across all 10 financial data categories.

## Summary Table

| # | Category | Primary Source | Backup Source | Free? | API Key? |
|---|----------|---------------|---------------|-------|----------|
| A | Equity Market Data | Yahoo Finance (yfinance) | Alpha Vantage | ✅ | Optional |
| B | Company Fundamentals | Alpha Vantage / SEC EDGAR | Financial Modeling Prep | ✅ | Yes (free) |
| C | ETF Data | Yahoo Finance | Alpha Vantage | ✅ | Optional |
| D | Forex & Currency | Frankfurter API (ECB) | ExchangeRate-API | ✅ | No! |
| E | Cryptocurrency | CoinGecko | CoinMarketCap | ✅ | No (basic) |
| F | Commodities | Alpha Vantage / Yahoo Finance | Quandl (Nasdaq) | ✅ | Yes (free) |
| G | Bonds & Fixed Income | FRED API (US Treasury) | RBI DBIE (India) | ✅ | Yes (free) |
| H | Indices & Benchmarks | Yahoo Finance | Alpha Vantage | ✅ | Optional |
| I | Economic/Macro Data | FRED API | World Bank Open Data | ✅ | Yes (free) |
| J | Financial Analytics | Self-computed (pandas-ta) | Alpha Vantage | ✅ | N/A |

---

## Category A: Equity Market Data

### Source 1: Yahoo Finance (via yfinance Python library)
- **URL:** https://finance.yahoo.com (Library: pip install yfinance)
- **Coverage:** 60+ countries, 100,000+ stocks, all major exchanges
- **Available Fields:** OHLCV (Open/High/Low/Close/Volume), dividends, splits, market cap, sector, industry, PE ratio, 52-week high/low
- **Extraction Method:** Python library (yfinance) — wraps Yahoo's unofficial API
- **Update Frequency:** Real-time (15-min delayed for free)
- **Historical Availability:** 20+ years for most stocks
- **Authentication:** None required
- **Rate Limits:** No official limit but aggressive scraping gets blocked
- **Commercial Usage:** ⚠️ Yahoo's TOS prohibit commercial redistribution of their data. Use only for development/prototyping. For production, use licensed data feeds.

### Source 2: Alpha Vantage
- **URL:** https://www.alphavantage.co
- **Coverage:** US stocks, some international (100+ exchanges)
- **Available Fields:** OHLCV, adjusted close, dividends, splits
- **Extraction Method:** REST API (JSON/CSV)
- **Update Frequency:** Real-time (free tier: end-of-day)
- **Historical Availability:** 20+ years daily, 1-2 months intraday
- **Authentication:** Free API key required
- **Rate Limits:** 25 requests/day (free), 75/min (premium)
- **Commercial Usage:** Free tier for personal use. Premium for commercial.

### Source 3: NSE India (Bhavcopy)
- **URL:** https://www.nseindia.com/reports
- **Coverage:** All NSE-listed Indian securities (~2000 stocks)
- **Available Fields:** OHLC, volume, delivery %, 52-week high/low
- **Extraction Method:** Daily CSV file download
- **Update Frequency:** Daily (after market close, ~6 PM IST)
- **Historical Availability:** 5+ years via archives
- **Authentication:** None (requires browser-like headers)
- **Commercial Usage:** ✅ Public data, free to use

---

## Category B: Company Financial Fundamentals

### Source 1: Alpha Vantage — Fundamentals Endpoints
- **URL:** https://www.alphavantage.co (functions: INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW)
- **Coverage:** US-listed companies (5000+)
- **Available Fields:** Revenue, net income, total assets, debt, EPS, operating cash flow, all line items from 10-K/10-Q filings
- **Extraction Method:** REST API (JSON)
- **Update Frequency:** Quarterly (after earnings filings)
- **Historical Availability:** 5+ years annual, 20+ quarters
- **Authentication:** Free API key
- **Rate Limits:** 25 requests/day (free)

### Source 2: SEC EDGAR (US SEC Filings)
- **URL:** https://efts.sec.gov/LATEST/search-index
- **Coverage:** All US publicly traded companies
- **Available Fields:** Complete 10-K, 10-Q, 8-K filings (XBRL format)
- **Extraction Method:** REST API + XBRL parsing
- **Update Frequency:** As filed (real-time)
- **Historical Availability:** 1993 onwards (EDGAR inception)
- **Authentication:** None (requires User-Agent header with email)
- **Commercial Usage:** ✅ 100% public domain — US government data

---

## Category C: ETF Data

### Source 1: Yahoo Finance (yfinance)
- **Coverage:** 10,000+ ETFs globally
- **Fields:** NAV, market price, expense ratio, holdings (top 10), AUM, inception date, category, fund family, returns (YTD, 1Y, 3Y, 5Y)
- **Method:** Python library
- **Commercial Usage:** ⚠️ Personal use only

---

## Category D: Forex & Currency Data ✅ (IMPLEMENTED)

### Source 1: Frankfurter API (Primary — Used in pipeline)
- **URL:** https://api.frankfurter.app
- **Coverage:** 33 currencies (EUR-based, converts all pairs)
- **Fields:** Base rate, target rate, date, amount
- **Method:** REST API (JSON), no authentication
- **Update:** Daily (ECB publishes ~4 PM CET on business days)
- **History:** 1999 onwards (Euro inception)
- **Commercial Usage:** ✅ Open source, MIT license, free forever

### Source 2: ExchangeRate-API
- **URL:** https://www.exchangerate-api.com
- **Coverage:** 160+ currencies
- **Fields:** Exchange rates, conversion
- **Method:** REST API
- **Free Tier:** 1,500 requests/month
- **Commercial Usage:** ✅ Allowed on paid plans

### Source 3: Open Exchange Rates
- **URL:** https://openexchangerates.org
- **Coverage:** 170+ currencies
- **Free Tier:** 1,000 requests/month, hourly updates
- **Commercial Usage:** ✅ Allowed on paid plans

---

## Category E: Cryptocurrency ✅ (IMPLEMENTED)

### Source 1: CoinGecko (Primary — Used in pipeline)
- **URL:** https://api.coingecko.com/api/v3
- **Coverage:** 13,000+ coins, 600+ exchanges
- **Fields:** Price, market cap, volume, supply, ATH, price change %, sparklines, OHLC, historical data
- **Method:** REST API (JSON)
- **Free Tier:** 10-30 calls/minute, no key needed (Demo API)
- **History:** Varies by coin (Bitcoin: 2013+)
- **Commercial Usage:** ✅ Free for personal, paid for commercial

### Source 2: CoinMarketCap
- **URL:** https://pro.coinmarketcap.com/api
- **Coverage:** 10,000+ coins
- **Free Tier:** 10,000 calls/month, basic endpoints
- **Commercial Usage:** ✅ Allowed on paid plans

---

## Category F: Commodities & Precious Metals

### Source 1: Alpha Vantage
- **Endpoint:** COMMODITY functions (WTI, BRENT, NATURAL_GAS, COPPER, etc.)
- **Fields:** Daily/weekly/monthly prices
- **History:** 10+ years
- **Rate Limit:** 25/day free

### Source 2: Yahoo Finance
- **Tickers:** GC=F (Gold), SI=F (Silver), CL=F (Crude Oil), NG=F (Gas)
- **Fields:** OHLCV for commodity futures
- **History:** 10+ years

---

## Category G: Bonds & Fixed Income ✅ (PARTIALLY IMPLEMENTED via FRED)

### Source 1: FRED API (Primary)
- **Series:** DGS10 (10Y Treasury), DGS2 (2Y), DGS30 (30Y), BAMLH0A0HYM2 (High Yield Spread)
- **Coverage:** US Treasury yields, corporate bond indices
- **History:** 1962 onwards for some series

### Source 2: RBI DBIE (India)
- **URL:** https://data.rbi.org.in
- **Coverage:** Indian G-Sec yields, T-bill rates
- **Method:** Web portal + Excel download + manual parsing
- **Commercial Usage:** ✅ Public government data

---

## Category H: Indices & Market Benchmarks

### Source 1: Yahoo Finance
- **Tickers:** ^GSPC (S&P 500), ^DJI (Dow), ^IXIC (NASDAQ), ^NSEI (Nifty 50), ^BSESN (Sensex), ^FTSE (FTSE 100)
- **Fields:** OHLCV, historical values
- **History:** 20+ years

---

## Category I: Economic & Macro Data ✅ (IMPLEMENTED)

### Source 1: FRED API (Primary — Used in pipeline)
- **URL:** https://api.stlouisfed.org/fred
- **Coverage:** 800,000+ series — GDP, CPI, unemployment, rates, production
- **Method:** REST API (JSON/XML)
- **History:** Some series from 1947
- **Commercial Usage:** ✅ 100% free, US government data

### Source 2: World Bank Open Data
- **URL:** https://api.worldbank.org/v2
- **Coverage:** 200+ countries, 1600+ indicators
- **Method:** REST API (JSON/XML), no key needed
- **History:** 1960 onwards for many indicators
- **Commercial Usage:** ✅ Creative Commons license

### Source 3: IMF Data
- **URL:** https://datahelp.imf.org/knowledgebase/articles/667681
- **Coverage:** Global macro data (WEO, IFS, DOTS)
- **Method:** REST API
- **Commercial Usage:** ✅ Free for non-commercial

---

## Category J: Financial Analytics APIs

### Source: Self-Computed (No External API Needed)
- **Library:** pandas-ta or ta-lib
- **What it computes:**
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - SMA/EMA (Simple/Exponential Moving Averages)
  - Bollinger Bands
  - Volatility (standard deviation of returns)
  - Max Drawdown
  - Sharpe Ratio
  - Correlation Matrix
- **Method:** Python calculation on stored price data
- **Rationale:** Stored price data in PostgreSQL enables native calculation without external API dependencies, recurring costs, or third-party rate limits.
