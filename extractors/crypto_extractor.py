import time
from typing import Dict, List, Any

from extractors.base_extractor import BaseExtractor
from config.settings import settings


class CryptoExtractor(BaseExtractor):

    def get_source_name(self) -> str:
        return "crypto"

    def extract(self) -> Dict[str, Any]:
        self.logger.info("Starting Crypto data extraction")
        result = {}

        result["market_data"] = self._extract_market_data()

        top_10_ids = [coin["id"] for coin in result["market_data"][:10]]
        result["historical_data"] = self._extract_historical_data(top_10_ids)

        self.logger.info(
            "Crypto extraction complete",
            coins_current=len(result["market_data"]),
            coins_historical=len(result["historical_data"])
        )

        return result

    def _extract_market_data(self) -> List[Dict]:
        url = f"{settings.COINGECKO_BASE_URL}/coins/markets"
        params = {
            "vs_currency": settings.CRYPTO_VS_CURRENCY,
            "order": "market_cap_desc",
            "per_page": settings.CRYPTO_TOP_N,
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "24h,7d,30d"
        }

        data = self._make_request(url, params=params)
        self._save_raw_response(data, "crypto_markets")

        self.logger.info("Market data extracted", coins=len(data))
        return data

    def _extract_historical_data(self, coin_ids: List[str]) -> Dict[str, Any]:
        historical = {}

        for coin_id in coin_ids:
            self.logger.info("Extracting historical data", coin=coin_id)

            url = f"{settings.COINGECKO_BASE_URL}/coins/{coin_id}/market_chart"
            params = {
                "vs_currency": settings.CRYPTO_VS_CURRENCY,
                "days": 365,
                "interval": "daily"
            }

            try:
                data = self._make_request(url, params=params)
                raw_id = self._save_raw_response(data, f"crypto_history_{coin_id}")
                data["_raw_id"] = raw_id
                historical[coin_id] = data

                self.logger.info(
                    "Historical data extracted",
                    coin=coin_id,
                    price_points=len(data.get("prices", []))
                )

            except Exception as e:
                self.logger.error(
                    "Failed to extract historical data",
                    coin=coin_id,
                    error=str(e)
                )
                continue

            time.sleep(2)

        return historical
