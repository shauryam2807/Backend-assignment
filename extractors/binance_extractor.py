import time
from typing import Dict, List, Any
from extractors.base_extractor import BaseExtractor


class BinanceExtractor(BaseExtractor):
    """
    Extracts high-resolution OHLCV klines from Binance Public API.
    Zero API key required; exactly matches Twelve Data's crypto source.
    """

    BASE_URL = "https://api.binance.com/api/v3"
    DEFAULT_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]

    def get_source_name(self) -> str:
        return "crypto"

    def extract(self, symbols: List[str] = None, interval: str = "1d", limit: int = 365) -> Dict[str, Any]:
        self.logger.info("Starting Binance OHLCV extraction")
        symbols = symbols or self.DEFAULT_SYMBOLS
        result = {}

        for sym in symbols:
            self.logger.info("Extracting klines for symbol", symbol=sym, interval=interval)
            url = f"{self.BASE_URL}/klines"
            params = {
                "symbol": sym,
                "interval": interval,
                "limit": limit
            }

            try:
                data = self._make_request(url, params=params)
                raw_id = self._save_raw_response(data, f"binance_klines_{sym.lower()}")
                result[sym] = {
                    "raw_id": raw_id,
                    "symbol": sym,
                    "interval": interval,
                    "klines": data
                }
                self.logger.info("Klines extracted", symbol=sym, candles=len(data))
            except Exception as e:
                self.logger.error("Failed to extract Binance klines", symbol=sym, error=str(e))
                continue

            time.sleep(0.5)

        return result

