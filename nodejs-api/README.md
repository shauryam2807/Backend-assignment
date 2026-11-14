# 🟢 MFAPIs — Node.js Express REST API (Twelve Data Compatible)

Institutional financial data REST API built in **Node.js (Express)** adhering strictly to the **Twelve Data API specification**.

## 🏗️ Architecture

```
Client / Trader / App
        │
        ▼
Express Router (twelvedata.routes.js)
        │
        ▼
Controller (price, quote, time_series, exchange_rate, eod)
        │
   ┌────┴────────────────────────┐
   ▼                             ▼
Live Service (Binance/Yahoo)   PostgreSQL 17 Models
(Real-Time Feeds + 30s Cache)  (Fallback & Historical)
```

## ⚙️ Tech Stack

- **Runtime:** Node.js (v18+)
- **Framework:** Express.js 4.x
- **Database Client:** `pg` (PostgreSQL Connection Pooling)
- **HTTP Client:** `axios`
- **Caching:** `node-cache` (In-memory 30s TTL)
- **Security:** `helmet` (HTTP headers), `express-rate-limit` (DDoS protection)
- **Logging:** `morgan` (HTTP request logger)
- **Testing:** Jest + Supertest (17+ automated tests)

## 🛡️ Production Middleware Stack

| Middleware | Purpose |
|-----------|---------|
| `helmet` | Secure HTTP headers (XSS, HSTS, CSP, Content-Type sniffing) |
| `cors` | Cross-origin resource sharing |
| `morgan` | HTTP request logging (`dev` in development, `combined` in production) |
| `express-rate-limit` | 100 requests per 15-min window per IP |
| `X-Response-Time` | Response time tracking header |
| `errorHandler` | Structured error responses with dev stack traces |

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd nodejs-api
npm install
```

### 2. Configure Environment
Create `.env` file (copied from `.env.example`):
```env
PORT=3000
DATABASE_URL=postgresql://postgres:password@localhost:5432/mfapis_db
NODE_ENV=development
```

### 3. Start the Server
```bash
# Production mode
npm start

# Development mode (auto-reload on code change)
npm run dev
```
Server runs at `http://localhost:3000`.

### 4. Run Automated Test Suite
```bash
npm test

# With coverage report
npm run test:coverage
```

## 🔗 Twelve Data Compatible Endpoints

| Endpoint | Method | Params | Example URL | Response Contract |
|---|---|---|---|---|
| `/time_series` | GET | `symbol`, `interval`, `outputsize` | `/time_series?symbol=BTC/USD&interval=1day&outputsize=30` | `{ meta: {...}, values: [...], status: "ok" }` |
| `/price` | GET | `symbol` | `/price?symbol=BTC/USD` | `{"price": "88450.20"}` |
| `/quote` | GET | `symbol` | `/quote?symbol=ETH/USD` | Snapshot with 52-week range |
| `/exchange_rate` | GET | `symbol` | `/exchange_rate?symbol=EUR/USD` | `{"symbol": "EUR/USD", "rate": 1.0852, "timestamp": ...}` |
| `/eod` | GET | `symbol` | `/eod?symbol=BTC/USD` | End of day candle |
| `/cryptocurrencies` | GET | — | `/cryptocurrencies` | Available crypto symbols |
| `/forex_pairs` | GET | — | `/forex_pairs` | Available forex pairs |
| `/health` | GET | — | `/health` | Health, DB status & system metadata |

## 📊 Health Check Response

The `/health` endpoint includes a live database connectivity probe:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "database": {
    "status": "connected",
    "latency_ms": 3
  },
  "uptime_seconds": 1234
}
```

## 🤖 CI/CD

The Node.js API has its own GitHub Actions workflow (`.github/workflows/nodejs-ci.yml`) that runs the test suite across Node.js 18, 20, and 22 on every push to `nodejs-api/`.
