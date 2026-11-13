"""
Services package — Real-time data fetching and caching layer.

Provides live market data from Binance (crypto) and Yahoo Finance (forex)
with a thread-safe TTL cache to prevent upstream rate limiting.
"""
from services.cache import cache, TTLCache
from services.live_fetcher import (
    fetch_live_crypto_price,
    fetch_live_crypto_kline,
    fetch_live_forex_rate,
    fetch_live_forex_candle,
)

__all__ = [
    "cache",
    "TTLCache",
    "fetch_live_crypto_price",
    "fetch_live_crypto_kline",
    "fetch_live_forex_rate",
    "fetch_live_forex_candle",
]
