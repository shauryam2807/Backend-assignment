"""
Unit tests for services/cache.py and services/live_fetcher.py.
All live API calls are mocked — no network access required.
"""
import time
import pytest
from unittest.mock import patch, MagicMock

from services.cache import TTLCache
from services.live_fetcher import (
    get_binance_ticker,
    get_forex_ticker,
    fetch_live_crypto_price,
    fetch_live_crypto_kline,
    fetch_live_forex_rate,
    fetch_live_forex_candle,
    CRYPTO_MAP,
    FOREX_MAP,
)


# =============================================================================
# TTLCache Tests
# =============================================================================

class TestTTLCache:
    def test_set_and_get(self):
        c = TTLCache(default_ttl=60)
        c.set("key1", 42)
        assert c.get("key1") == 42

    def test_expiry(self):
        c = TTLCache(default_ttl=1)
        c.set("temp", "value", ttl=1)
        assert c.get("temp") == "value"
        time.sleep(1.1)
        assert c.get("temp") is None

    def test_get_missing_key(self):
        c = TTLCache()
        assert c.get("nonexistent") is None

    def test_overwrite(self):
        c = TTLCache()
        c.set("k", "v1")
        c.set("k", "v2")
        assert c.get("k") == "v2"

    def test_clear(self):
        c = TTLCache()
        c.set("a", 1)
        c.set("b", 2)
        c.clear()
        assert c.get("a") is None
        assert c.get("b") is None

    def test_size(self):
        c = TTLCache(default_ttl=60)
        c.set("x", 10)
        c.set("y", 20)
        assert c.size() == 2

    def test_size_excludes_expired(self):
        c = TTLCache()
        c.set("live", "ok", ttl=60)
        c.set("dead", "gone", ttl=1)
        time.sleep(1.1)
        assert c.size() == 1

    def test_cleanup(self):
        c = TTLCache()
        c.set("keep", 1, ttl=60)
        c.set("expire1", 2, ttl=1)
        c.set("expire2", 3, ttl=1)
        time.sleep(1.1)
        removed = c.cleanup()
        assert removed == 2
        assert c.get("keep") == 1

    def test_custom_ttl_per_key(self):
        c = TTLCache(default_ttl=60)
        c.set("short", "s", ttl=1)
        c.set("long", "l", ttl=60)
        time.sleep(1.1)
        assert c.get("short") is None
        assert c.get("long") == "l"


# =============================================================================
# Symbol Mapping Tests
# =============================================================================

class TestSymbolMapping:
    def test_crypto_map_standard(self):
        assert get_binance_ticker("BTC/USD") == "BTCUSDT"
        assert get_binance_ticker("ETH/USD") == "ETHUSDT"

    def test_crypto_map_short(self):
        assert get_binance_ticker("BTC") == "BTCUSDT"
        assert get_binance_ticker("SOL") == "SOLUSDT"

    def test_forex_returns_none_for_binance(self):
        """Forex symbols must NOT resolve to a Binance ticker."""
        assert get_binance_ticker("EUR/USD") is None
        assert get_binance_ticker("GBP/USD") is None
        assert get_binance_ticker("USD/JPY") is None

    def test_forex_ticker(self):
        assert get_forex_ticker("EUR/USD") == "EURUSD=X"
        assert get_forex_ticker("GBP/USD") == "GBPUSD=X"

    def test_forex_ticker_unknown_pair(self):
        # Unknown pairs still get a ticker constructed
        assert get_forex_ticker("NZD/USD") == "NZDUSD=X"

    def test_case_insensitive(self):
        assert get_binance_ticker("btc/usd") == "BTCUSDT"
        assert get_forex_ticker("eur/usd") == "EURUSD=X"


# =============================================================================
# Live Fetcher Tests (mocked network)
# =============================================================================

class TestFetchLiveCryptoPrice:
    @patch("services.live_fetcher.cache")
    @patch("services.live_fetcher.requests.get")
    def test_success(self, mock_get, mock_cache):
        mock_cache.get.return_value = None
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"symbol": "BTCUSDT", "price": "90123.45"}
        mock_get.return_value = mock_resp

        result = fetch_live_crypto_price("BTC/USD")
        assert result == 90123.45
        mock_cache.set.assert_called_once()

    @patch("services.live_fetcher.cache")
    def test_cached(self, mock_cache):
        mock_cache.get.return_value = 88000.0
        result = fetch_live_crypto_price("BTC/USD")
        assert result == 88000.0

    def test_forex_symbol_returns_none(self):
        result = fetch_live_crypto_price("EUR/USD")
        assert result is None

    @patch("services.live_fetcher.cache")
    @patch("services.live_fetcher.requests.get")
    def test_api_error(self, mock_get, mock_cache):
        mock_cache.get.return_value = None
        mock_get.side_effect = ConnectionError("timeout")
        result = fetch_live_crypto_price("BTC/USD")
        assert result is None


class TestFetchLiveCryptoKline:
    @patch("services.live_fetcher.cache")
    @patch("services.live_fetcher.requests.get")
    def test_success(self, mock_get, mock_cache):
        mock_cache.get.return_value = None
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = [
            [1700000000000, "90000.0", "91000.0", "89000.0", "90500.0", "100.5"]
        ]
        mock_get.return_value = mock_resp

        result = fetch_live_crypto_kline("BTC/USD")
        assert result is not None
        assert result["open"] == "90000.00"
        assert result["close"] == "90500.00"
        assert "datetime" in result

    @patch("services.live_fetcher.cache")
    @patch("services.live_fetcher.requests.get")
    def test_interval_mapping(self, mock_get, mock_cache):
        mock_cache.get.return_value = None
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = [
            [1700000000000, "90000.0", "91000.0", "89000.0", "90500.0", "100.5"]
        ]
        mock_get.return_value = mock_resp

        fetch_live_crypto_kline("BTC/USD", interval="1min")
        # Verify the URL used 1m interval
        call_url = mock_get.call_args[0][0]
        assert "interval=1m" in call_url


class TestFetchLiveForexRate:
    @patch("services.live_fetcher.cache")
    @patch("services.live_fetcher.requests.get")
    def test_success(self, mock_get, mock_cache):
        mock_cache.get.return_value = None
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "chart": {
                "result": [{
                    "meta": {"regularMarketPrice": 1.08523}
                }]
            }
        }
        mock_get.return_value = mock_resp

        result = fetch_live_forex_rate("EUR/USD")
        assert result == 1.08523

    @patch("services.live_fetcher.cache")
    @patch("services.live_fetcher.requests.get")
    def test_api_error(self, mock_get, mock_cache):
        mock_cache.get.return_value = None
        mock_get.side_effect = ConnectionError("network unreachable")
        result = fetch_live_forex_rate("EUR/USD")
        assert result is None


class TestFetchLiveForexCandle:
    @patch("services.live_fetcher.cache")
    @patch("services.live_fetcher.requests.get")
    def test_success(self, mock_get, mock_cache):
        mock_cache.get.return_value = None
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "chart": {
                "result": [{
                    "timestamp": [1700000000],
                    "indicators": {
                        "quote": [{
                            "open": [1.0850],
                            "high": [1.0920],
                            "low": [1.0810],
                            "close": [1.0890],
                            "volume": [0]
                        }]
                    }
                }]
            }
        }
        mock_get.return_value = mock_resp

        result = fetch_live_forex_candle("EUR/USD")
        assert result is not None
        assert result["open"] == "1.08500"
        assert result["close"] == "1.08900"
        assert "datetime" in result

    @patch("services.live_fetcher.cache")
    @patch("services.live_fetcher.requests.get")
    def test_null_candle_skip(self, mock_get, mock_cache):
        """Should skip null candles and find last valid one."""
        mock_cache.get.return_value = None
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "chart": {
                "result": [{
                    "timestamp": [1700000000, 1700086400],
                    "indicators": {
                        "quote": [{
                            "open": [1.0850, None],
                            "high": [1.0920, None],
                            "low": [1.0810, None],
                            "close": [1.0890, None],
                            "volume": [0, 0]
                        }]
                    }
                }]
            }
        }
        mock_get.return_value = mock_resp

        result = fetch_live_forex_candle("EUR/USD")
        assert result is not None
        # Should pick the first (valid) candle, not the null one
        assert result["close"] == "1.08900"

