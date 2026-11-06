from typing import Dict, List, Any

from extractors.base_extractor import BaseExtractor
from config.settings import settings


class EconomicExtractor(BaseExtractor):

    def get_source_name(self) -> str:
        return "economic"

    def extract(self) -> Dict[str, Any]:
        self.logger.info("Starting Economic data extraction")

        if not settings.FRED_API_KEY:
            self.logger.error(
                "FRED API key not configured! "
                "Get free key from: https://fred.stlouisfed.org/docs/api/api_key.html"
            )
            raise ValueError("FRED_API_KEY not set in .env file")

        result = {}

        for indicator_id, indicator_info in settings.ECONOMIC_INDICATORS.items():
            self.logger.info(
                "Extracting indicator",
                indicator=indicator_id,
                name=indicator_info["name"]
            )

            try:
                metadata = self._extract_series_metadata(indicator_id)
                observations = self._extract_observations(indicator_id)

                result[indicator_id] = {
                    "metadata": metadata,
                    "observations": observations,
                    "config": indicator_info
                }

                self.logger.info(
                    "Indicator extracted",
                    indicator=indicator_id,
                    observations=len(observations.get("observations", []))
                )

            except Exception as e:
                self.logger.error(
                    "Failed to extract indicator",
                    indicator=indicator_id,
                    error=str(e)
                )
                continue

        self.logger.info(
            "Economic extraction complete",
            indicators=len(result)
        )

        return result

    def _extract_series_metadata(self, series_id: str) -> Dict:
        url = f"{settings.FRED_BASE_URL}/series"
        params = {
            "series_id": series_id,
            "api_key": settings.FRED_API_KEY,
            "file_type": "json"
        }

        data = self._make_request(url, params=params)
        self._save_raw_response(data, f"econ_metadata_{series_id.lower()}")
        return data

    def _extract_observations(self, series_id: str) -> Dict:
        url = f"{settings.FRED_BASE_URL}/series/observations"
        params = {
            "series_id": series_id,
            "api_key": settings.FRED_API_KEY,
            "file_type": "json",
            "sort_order": "asc"
        }

        data = self._make_request(url, params=params)
        raw_id = self._save_raw_response(data, f"econ_observations_{series_id.lower()}")
        data["_raw_id"] = raw_id
        return data
