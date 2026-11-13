"""
Live financial data fetcher for Binance (Crypto) and Yahoo Finance (Forex).
Directly queries institutional feeds in real-time with zero mocking.
"""
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import requests

from config.logging_config import get_logger
from services.cache import cache

logger = get_logger("live_fetcher")

CRYPTO_MAP = {
    "BTC/USD": "BTCUSDT",
    "ETH/USD": "ETHUSDT",
    "SOL/USD": "SOLUSDT",
    "BNB/USD": "BNBUSDT",
    "XRP/USD": "XRPUSDT",
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "SOL": "SOLUSDT",
    "BNB": "BNBUSDT",
    "XRP": "XRPUSDT",
}

FOREX_MAP = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "USDJPY=X",
    "USD/INR": "USDINR=X",
    "USD/CAD": "USDCAD=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CHF": "USDCHF=X",
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def get_binance_ticker(symbol: str) -> Optional[str]:
    clean = symbol.upper().strip()
    # Reject forex symbols — they must never hit Binance
    if clean in FOREX_MAP:
        return None
    if clean in CRYPTO_MAP:
        return CRYPTO_MAP[clean]
    if "/" in clean:
        base, quote = clean.split("/", 1)
        # Reject known fiat base currencies (forex pairs)
        if base in ("EUR", "GBP", "JPY", "INR", "CAD", "AUD", "CHF", "NZD", "SGD", "HKD"):
            return None
        if quote in ("USD", "USDT"):
            return f"{base}USDT"
    return None


def get_forex_ticker(pair: str) -> Optional[str]:
    clean = pair.upper().strip()
    if clean in FOREX_MAP:
        return FOREX_MAP[clean]
    if "/" in clean:
        base, target = clean.split("/", 1)
        return f"{base}{target}=X"
    return None


def fetch_live_crypto_price(symbol: str) -> Optional[float]:
    """Fetch current real-time close/spot price from Binance."""
    ticker = get_binance_ticker(symbol)
    if not ticker:
        return None

    cache_key = f"crypto_price:{ticker}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    url = f"https://api.binance.com/api/v3/ticker/price?symbol={ticker}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            price = float(data.get("price", 0))
            if price > 0:
                cache.set(cache_key, price, ttl=30)
                return price
        else:
            logger.warning("binance_price_http_error", ticker=ticker, status=resp.status_code)
    except Exception as exc:
        logger.warning("binance_price_fetch_failed", ticker=ticker, error=str(exc))
    return None


def fetch_live_crypto_kline(symbol: str, interval: str = "1d") -> Optional[Dict[str, Any]]:
    """Fetch the latest active/current daily candle from Binance."""
    ticker = get_binance_ticker(symbol)
    if not ticker:
        return None

    # Binance interval mapping
    b_interval = "1d"
    if interval in ("1min", "1m"):
        b_interval = "1m"
    elif interval in ("5min", "5m"):
        b_interval = "5m"
    elif interval in ("15min", "15m"):
        b_interval = "15m"
    elif interval in ("1h", "1hour"):
        b_interval = "1h"
    elif interval in ("1week", "1w"):
        b_interval = "1w"

    cache_key = f"crypto_kline:{ticker}:{b_interval}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    url = f"https://api.binance.com/api/v3/klines?symbol={ticker}&interval={b_interval}&limit=1"
    try:

        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            klines = resp.json()
            if klines and len(klines) > 0 and len(klines[0]) >= 6:
                c = klines[0]
                candle_date = datetime.fromtimestamp(c[0] / 1000, tz=timezone.utc).date()
                candle = {
                    "datetime": str(candle_date),
                    "open": f"{float(c[1]):.2f}",
                    "high": f"{float(c[2]):.2f}",
                    "low": f"{float(c[3]):.2f}",
                    "close": f"{float(c[4]):.2f}",
                    "volume": f"{int(float(c[5]))}"
                }
                cache.set(cache_key, candle, ttl=30)
                return candle
        else:
            logger.warning("binance_kline_http_error", ticker=ticker, status=resp.status_code)
    except Exception as exc:
        logger.warning("binance_kline_fetch_failed", ticker=ticker, error=str(exc))
    return None


def fetch_live_forex_rate(pair: str) -> Optional[float]:
    """Fetch current real-time exchange rate from Yahoo Finance."""
    ticker = get_forex_ticker(pair)
    if not ticker:
        return None

    cache_key = f"forex_rate:{ticker}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1d&interval=1m"
    headers = {"User-Agent": USER_AGENT}
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            result = data.get("chart", {}).get("result", [])
            if result:
                meta = result[0].get("meta", {})
                price = meta.get("regularMarketPrice")
                if price and float(price) > 0:
                    rate = round(float(price), 5)
                    cache.set(cache_key, rate, ttl=30)
                    return rate
        else:
            logger.warning("yahoo_rate_http_error", ticker=ticker, status=resp.status_code)
    except Exception as exc:
        logger.warning("yahoo_rate_fetch_failed", ticker=ticker, error=str(exc))
    return None


def fetch_live_forex_candle(pair: str) -> Optional[Dict[str, Any]]:
    """Fetch the latest active daily candle from Yahoo Finance."""
    ticker = get_forex_ticker(pair)
    if not ticker:
        return None

    cache_key = f"forex_candle:{ticker}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=5d&interval=1d"
    headers = {"User-Agent": USER_AGENT}
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            result = data.get("chart", {}).get("result", [])
            if result:
                res = result[0]
                timestamps = res.get("timestamp", [])
                quotes = res.get("indicators", {}).get("quote", [{}])[0]
                opens = quotes.get("open", [])
                highs = quotes.get("high", [])
                lows = quotes.get("low", [])
                closes = quotes.get("close", [])
                volumes = quotes.get("volume", [])

                # find last valid non-null candle
                for i in range(len(timestamps) - 1, -1, -1):
                    o = opens[i] if i < len(opens) else None
                    h = highs[i] if i < len(highs) else None
                    l = lows[i] if i < len(lows) else None
                    c = closes[i] if i < len(closes) else None
                    if all(v is not None for v in (o, h, l, c)):
                        candle_date = datetime.fromtimestamp(timestamps[i], tz=timezone.utc).date()
                        candle = {
                            "datetime": str(candle_date),
                            "open": f"{float(o):.5f}",
                            "high": f"{float(h):.5f}",
                            "low": f"{float(l):.5f}",
                            "close": f"{float(c):.5f}",
                            "volume": f"{int(float(volumes[i] or 0)) if i < len(volumes) else 0}"
                        }
                        cache.set(cache_key, candle, ttl=30)
                        return candle
        else:
            logger.warning("yahoo_candle_http_error", ticker=ticker, status=resp.status_code)
    except Exception as exc:
        logger.warning("yahoo_candle_fetch_failed", ticker=ticker, error=str(exc))
    return None
