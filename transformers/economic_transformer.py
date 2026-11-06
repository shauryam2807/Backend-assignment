from typing import Dict, Any

import pandas as pd

from transformers.base_transformer import BaseTransformer
from config.settings import settings


class EconomicTransformer(BaseTransformer):

    def transform(self, raw_data: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        self.logger.info("Starting Economic data transformation")

        indicators_rows = []
        values_rows = []

        for indicator_id, data in raw_data.items():
            metadata = data.get("metadata", {})
            config = data.get("config", {})
            indicator_meta = self._transform_metadata(indicator_id, metadata, config)
            if indicator_meta:
                indicators_rows.append(indicator_meta)

            observations = data.get("observations", {})
            raw_id = observations.get("_raw_id")
            obs_list = observations.get("observations", [])

            for obs in obs_list:
                value = self._safe_float(obs.get("value"))
                obs_date = self._safe_date(obs.get("date"))

                if obs_date is not None:
                    values_rows.append({
                        "indicator_id": indicator_id,
                        "observation_date": obs_date,
                        "value": value,
                        "country": "US",
                        "source": "fred",
                        "raw_response_id": raw_id
                    })

        indicators_df = pd.DataFrame(indicators_rows)
        values_df = pd.DataFrame(values_rows)

        if not values_df.empty:
            values_df = values_df.drop_duplicates(
                subset=["indicator_id", "observation_date"],
                keep="last"
            )

        self.logger.info(
            "Economic transformation complete",
            indicators=len(indicators_df),
            values=len(values_df)
        )

        return {
            "indicators": indicators_df,
            "values": values_df
        }

    def _transform_metadata(
        self, indicator_id: str, metadata: Dict, config: Dict
    ) -> Dict:
        seriess = metadata.get("seriess", [])
        if not seriess:
            return {
                "indicator_id": indicator_id,
                "name": config.get("name", indicator_id),
                "frequency": config.get("frequency"),
                "category": config.get("category"),
                "source": "fred"
            }

        series = seriess[0]
        return {
            "indicator_id": indicator_id,
            "name": series.get("title", config.get("name", "")),
            "description": series.get("notes", ""),
            "frequency": series.get("frequency", "").lower(),
            "units": series.get("units", ""),
            "seasonal_adjustment": series.get("seasonal_adjustment", ""),
            "country": "US",
            "category": config.get("category", ""),
            "source_agency": series.get("source", ""),
            "source": "fred",
            "is_active": True
        }
