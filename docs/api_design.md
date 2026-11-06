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

## SDK Example (Python)

```python
import requests

API_KEY = "your_api_key"
BASE_URL = "https://api.mfapis.com/v1"

response = requests.get(
    f"{BASE_URL}/forex/rates/latest",
    headers={"X-API-Key": API_KEY},
    params={"base": "USD", "targets": "EUR,GBP,INR"}
)

data = response.json()
print(f"USD to INR: {data['data']['INR']}")
```
