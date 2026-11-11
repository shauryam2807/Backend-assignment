# MFAPIs — REST API Design (v1)

## Base URL
```
https://api.mfapis.com/v1
```

## Authentication
All endpoints require an API key via header:
```
X-API-Key: your_api_key_here
```

## Rate Limits
| Tier | Requests/Minute | Daily Limit |
|------|----------------|-------------|
| Free | 30 | 1,000 |
| Starter | 120 | 10,000 |
| Pro | 600 | 100,000 |
| Enterprise | Unlimited | Unlimited |

Rate limit headers returned with every response:
```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 28
X-RateLimit-Reset: 1730000000
```

---

## Standard Response Envelope

All endpoints return this consistent structure:

```json
{
  "status": "success",
  "meta": {
    "source": "frankfurter",
    "total_records": 100,
    "page": 1,
    "per_page": 25,
    "total_pages": 4,
    "generated_at": "2026-11-05T17:00:00Z"
  },
  "data": [...]
}
```

## Error Response Format
```json
{
  "status": "error",
  "error": {
    "code": 429,
    "message": "Rate limit exceeded. Please wait 30 seconds.",
    "retry_after": 30
  }
}
```

| Status Code | Meaning |
|-------------|---------|
| 200 | Success |
| 400 | Bad Request — invalid parameters |
| 401 | Unauthorized — missing or invalid API key |
| 404 | Not Found — resource does not exist |
| 429 | Too Many Requests — rate limit exceeded |
| 500 | Internal Server Error |

---

## Endpoints

### Health Check

#### `GET /v1/health`
Returns API status and uptime.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 86400,
  "database": "connected",
  "timestamp": "2026-11-05T17:00:00Z"
}
```

---

### Forex Endpoints

#### `GET /v1/forex/pairs`
List all available currency pairs.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `base` | string | — | Filter by base currency (e.g., `USD`) |
| `is_active` | bool | true | Filter active/inactive pairs |

**Response:**
```json
{
  "status": "success",
  "meta": {"total_records": 145, "source": "frankfurter"},
  "data": [
    {
      "base_currency": "USD",
      "target_currency": "EUR",
      "pair_name": "USD/EUR",
      "is_active": true
    }
  ]
}
```

#### `GET /v1/forex/rates/latest`
Get latest exchange rates.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `base` | string | `USD` | Base currency |
| `targets` | string | all | Comma-separated target currencies |

**Response:**
```json
{
  "status": "success",
  "meta": {"source": "frankfurter", "base": "USD", "date": "2026-11-05"},
  "data": {
    "EUR": 0.9215,
    "GBP": 0.7891,
    "JPY": 149.32,
    "INR": 84.12
  }
}
```

#### `GET /v1/forex/rates/historical`
Get historical exchange rates for a date range.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `base` | string | `USD` | Base currency |
| `target` | string | required | Target currency |
| `start_date` | date | 30 days ago | Start date (YYYY-MM-DD) |
| `end_date` | date | today | End date (YYYY-MM-DD) |
| `page` | int | 1 | Page number |
| `per_page` | int | 25 | Records per page (max 100) |

**Response:**
```json
{
  "status": "success",
  "meta": {"total_records": 255, "page": 1, "per_page": 25},
  "data": [
    {"date": "2026-11-05", "base": "USD", "target": "EUR", "rate": 0.9215},
    {"date": "2026-11-04", "base": "USD", "target": "EUR", "rate": 0.9198}
  ]
}
```

#### `GET /v1/forex/convert`
Convert an amount between currencies.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `from` | string | required | Source currency |
| `to` | string | required | Target currency |
| `amount` | float | 1.0 | Amount to convert |

**Response:**
```json
{
  "status": "success",
  "data": {
    "from": "USD",
    "to": "INR",
    "amount": 100.0,
    "converted": 8412.50,
    "rate": 84.125,
    "date": "2026-11-05"
  }
}
```

---

### Crypto Endpoints

#### `GET /v1/crypto/coins`
List all tracked cryptocurrencies.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `limit` | int | 25 | Number of coins (max 100) |
| `order` | string | `market_cap_desc` | Sort order: `market_cap_desc`, `market_cap_asc`, `name_asc` |

**Response:**
```json
{
  "status": "success",
  "meta": {"total_records": 50, "source": "coingecko"},
  "data": [
    {
      "coin_id": "bitcoin",
      "symbol": "BTC",
      "name": "Bitcoin",
      "market_cap_rank": 1,
      "is_active": true,
      "image_url": "https://..."
    }
  ]
}
```

#### `GET /v1/crypto/prices/latest`
Get latest prices for top cryptocurrencies.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `coins` | string | top 10 | Comma-separated coin IDs |

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "coin_id": "bitcoin",
      "symbol": "BTC",
      "price_usd": 95234.50,
      "market_cap_usd": 1890000000000,
      "volume_24h_usd": 45000000000,
      "price_change_24h": 2.35,
      "date": "2026-11-05"
    }
  ]
}
```

#### `GET /v1/crypto/prices/historical`
Get historical price data for a coin.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `coin` | string | required | Coin ID (e.g., `bitcoin`) |
| `start_date` | date | 30 days ago | Start date |
| `end_date` | date | today | End date |
| `page` | int | 1 | Page number |
| `per_page` | int | 25 | Records per page |

**Response:**
```json
{
  "status": "success",
  "meta": {"coin": "bitcoin", "total_records": 365, "page": 1},
  "data": [
    {
      "date": "2026-11-05",
      "price_usd": 95234.50,
      "market_cap_usd": 1890000000000,
      "volume_usd": 45000000000
    }
  ]
}
```

#### `GET /v1/crypto/markets`
Get market overview with rankings.

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_coins_tracked": 50,
    "total_market_cap_usd": 3200000000000,
    "top_gainers_24h": [{"coin_id": "solana", "change": 8.5}],
    "top_losers_24h": [{"coin_id": "dogecoin", "change": -3.2}]
  }
}
```

---

### Economic Endpoints

#### `GET /v1/economic/indicators`
List all tracked economic indicators.

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "indicator_id": "GDP",
      "name": "Gross Domestic Product",
      "category": "GDP",
      "frequency": "quarterly",
      "units": "Billions of Dollars",
      "country": "US",
      "source_agency": "U.S. Bureau of Economic Analysis"
    }
  ]
}
```

#### `GET /v1/economic/data`
Get time series data for an indicator.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `indicator` | string | required | Indicator ID (e.g., `GDP`, `UNRATE`, `CPIAUCSL`) |
| `start_date` | date | all | Start date |
| `end_date` | date | today | End date |
| `page` | int | 1 | Page number |
| `per_page` | int | 50 | Records per page |

**Response:**
```json
{
  "status": "success",
  "meta": {
    "indicator": "UNRATE",
    "name": "Unemployment Rate",
    "units": "Percent",
    "frequency": "monthly",
    "total_records": 945
  },
  "data": [
    {"date": "2026-10-01", "value": 4.1},
    {"date": "2026-09-01", "value": 4.2}
  ]
}
```

---

## Twelve Data Compatible Endpoints

These endpoints match the Twelve Data API contract exactly, serving real OHLCV data from Binance (crypto) and Yahoo Finance (forex).

### `GET /time_series`

Returns OHLCV candle data in Twelve Data standard format.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `symbol` | string | required | Symbol (e.g., `BTC/USD`, `EUR/USD`) |
| `interval` | string | `1day` | Candle interval |
| `outputsize` | int | `30` | Number of candles (max 5000) |

**Response:**
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

### `GET /quote`

Returns a real-time quote snapshot with change calculation and 52-week range.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `symbol` | string | required | Symbol (e.g., `BTC/USD`, `EUR/USD`) |

**Response:**
```json
{
  "symbol": "BTC/USD",
  "name": "BTC / USD",
  "exchange": "Binance",
  "datetime": "2026-11-09",
  "open": "76450.00",
  "high": "77200.00",
  "low": "75800.00",
  "close": "76900.00",
  "volume": "12345",
  "previous_close": "76200.00",
  "change": "+700.00",
  "percent_change": "+0.9186",
  "fifty_two_week": {
    "low": "52100.00",
    "high": "99800.00"
  }
}
```

### `GET /price`

Returns the latest close price for a symbol.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `symbol` | string | required | Symbol (e.g., `BTC/USD`) |

**Response:**
```json
{"price": "76900.00"}
```

### `GET /exchange_rate`

Returns the latest exchange rate between two currencies.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `symbol` | string | required | Pair (e.g., `EUR/USD`) |

**Response:**
```json
{
  "symbol": "EUR/USD",
  "rate": 1.08912,
  "timestamp": 1731100800
}
```

### `GET /eod`

Returns end-of-day OHLCV data for a symbol.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `symbol` | string | required | Symbol (e.g., `BTC/USD`) |

**Response:**
```json
{
  "symbol": "BTC/USD",
  "exchange": "Binance",
  "datetime": "2026-11-09",
  "close": "76900.00",
  "open": "76450.00",
  "high": "77200.00",
  "low": "75800.00",
  "volume": "12345"
}
```

### `GET /cryptocurrencies`

Returns list of available cryptocurrency symbols.

### `GET /forex_pairs`

Returns list of available forex currency pairs.

---

## Data Sources

| Asset Class | Source | API Key Required |
|-------------|--------|-----------------|
| Crypto OHLCV | Binance Public API | No |
| Forex OHLC | Yahoo Finance Chart API | No |
| Forex Rates | Frankfurter (ECB) | No |
| Crypto Market | CoinGecko | No |
| Economic | FRED (St. Louis Fed) | Yes (free) |

---

## SDK Example (Python)

```python
import requests

# Twelve Data compatible endpoint (no auth required for demo)
BASE_URL = "http://localhost:10000"

# Get BTC/USD time series
response = requests.get(
    f"{BASE_URL}/time_series",
    params={"symbol": "BTC/USD", "interval": "1day", "outputsize": 10}
)
data = response.json()
print(f"Latest BTC close: {data['values'][0]['close']}")

# Get EUR/USD exchange rate
response = requests.get(
    f"{BASE_URL}/exchange_rate",
    params={"symbol": "EUR/USD"}
)
rate = response.json()
print(f"EUR/USD rate: {rate['rate']}")
```
