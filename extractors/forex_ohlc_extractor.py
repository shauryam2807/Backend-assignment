import time
from typing import Dict, List, Any
from extractors.base_extractor import BaseExtractor


class ForexOHLCExtractor(BaseExtractor):
    """
    Extracts real daily OHLC candles for Forex currency pairs.
    Uses institutional chart feeds (Yahoo Finance / Interbank) with zero API key required.
    """

    PAIR_MAP = {
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
        "USD/JPY": "USDJPY=X",
        "USD/INR": "USDINR=X",
        "USD/CAD": "USDCAD=X",
        "AUD/USD": "AUDUSD=X",
        "USD/CHF": "USDCHF=X"
    }

    def get_source_name(self) -> str:
        return "forex"

    def extract(self, pairs: List[str] = None, range_days: str = "1y") -> Dict[str, Any]:
        self.logger.info("Starting Forex OHLC extraction")
        pairs = pairs or list(self.PAIR_MAP.keys())
        result = {}

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        for pair in pairs:
            ticker = self.PAIR_MAP.get(pair, f"{pair.replace('/', '')}=X")
            self.logger.info("Extracting Forex OHLC", pair=pair, ticker=ticker)
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            params = {
                "range": range_days,
                "interval": "1d"
            }

            try:
                data = self._make_request(url, params=params, headers=headers)
                raw_id = self._save_raw_response(data, f"forex_ohlc_{pair.replace('/', '_').lower()}")
                result[pair] = {
                    "raw_id": raw_id,
                    "pair": pair,
                    "ticker": ticker,
                    "chart": data
                }
                self.logger.info("Forex OHLC extracted", pair=pair)
            except Exception as e:
                self.logger.error("Failed to extract Forex OHLC", pair=pair, error=str(e))
                continue

            time.sleep(0.5)

        return result

