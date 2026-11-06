from datetime import date, timedelta
from typing import Dict, List, Any

import pandas as pd

from extractors.base_extractor import BaseExtractor
from config.settings import settings


class ForexExtractor(BaseExtractor):

    def get_source_name(self) -> str:
        return "forex"

    def extract(self) -> Dict[str, Any]:
        self.logger.info("Starting Forex data extraction")
        result = {}

        result["currencies"] = self._extract_currencies()
        result["latest_rates"] = self._extract_latest_rates()
        result["historical_rates"] = self._extract_historical_rates(days=365)

        self.logger.info(
            "Forex extraction complete",
            currencies=len(result["currencies"]),
            latest_pairs=sum(len(v) for v in result["latest_rates"].values()),
            historical_days=len(result["historical_rates"])
        )

        return result

    def _extract_currencies(self) -> Dict[str, str]:
        url = f"{settings.FRANKFURTER_BASE_URL}/currencies"
        data = self._make_request(url)
        self._save_raw_response(data, "forex_currencies")
        self.logger.info("Currencies extracted", count=len(data))
        return data

    def _extract_latest_rates(self) -> Dict[str, Dict]:
        all_latest = {}

        for base_currency in settings.FOREX_BASE_CURRENCIES:
            targets = [c for c in settings.FOREX_TARGET_CURRENCIES if c != base_currency]
            targets_str = ",".join(targets)

            url = f"{settings.FRANKFURTER_BASE_URL}/latest"
            params = {"from": base_currency, "to": targets_str}

            try:
                data = self._make_request(url, params=params)
                self._save_raw_response(data, f"forex_latest_{base_currency.lower()}")
                all_latest[base_currency] = data
                self.logger.info(
                    "Latest rates extracted",
                    base=base_currency,
                    pairs=len(data.get("rates", {}))
                )
            except Exception as e:
                self.logger.error(
                    "Failed to extract latest rates",
                    base=base_currency,
                    error=str(e)
                )
                continue

        return all_latest

    def _extract_historical_rates(self, days: int = 365) -> List[Dict]:
        all_historical = []

        end_date = date.today()
        start_date = end_date - timedelta(days=days)

        for base_currency in ["USD", "EUR"]:
            targets = [c for c in settings.FOREX_TARGET_CURRENCIES if c != base_currency]
            targets_str = ",".join(targets)

            url = f"{settings.FRANKFURTER_BASE_URL}/{start_date}..{end_date}"
            params = {"from": base_currency, "to": targets_str}

            try:
                data = self._make_request(url, params=params)
                raw_id = self._save_raw_response(
                    data, f"forex_historical_{base_currency.lower()}"
                )

                data["_raw_id"] = raw_id
                data["_base_currency"] = base_currency
                all_historical.append(data)

                self.logger.info(
                    "Historical rates extracted",
                    base=base_currency,
                    start=str(start_date),
                    end=str(end_date),
                    days=len(data.get("rates", {}))
                )
            except Exception as e:
                self.logger.error(
                    "Failed to extract historical rates",
                    base=base_currency,
                    error=str(e)
                )
                continue

        return all_historical
