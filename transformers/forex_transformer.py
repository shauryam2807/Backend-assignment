from datetime import date
from typing import Dict, Any, List

import pandas as pd

from transformers.base_transformer import BaseTransformer


class ForexTransformer(BaseTransformer):

    def transform(self, raw_data: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        self.logger.info("Starting Forex data transformation")

        pairs_df = self._transform_pairs(raw_data.get("currencies", {}))
        latest_df = self._transform_latest(raw_data.get("latest_rates", {}))
        historical_df = self._transform_historical(raw_data.get("historical_rates", []))

        if not latest_df.empty and not historical_df.empty:
            daily_rates_df = pd.concat([historical_df, latest_df], ignore_index=True)
        elif not latest_df.empty:
            daily_rates_df = latest_df
        else:
            daily_rates_df = historical_df

        if not daily_rates_df.empty:
            daily_rates_df = daily_rates_df.drop_duplicates(
                subset=["base_currency", "target_currency", "rate_date"],
                keep="last"
            )

        self.logger.info(
            "Forex transformation complete",
            pairs=len(pairs_df),
            daily_rates=len(daily_rates_df)
        )

        return {
            "pairs": pairs_df,
            "daily_rates": daily_rates_df
        }

    def _transform_pairs(self, currencies: Dict[str, str]) -> pd.DataFrame:
        pairs = []
        base_currencies = ["USD", "EUR", "GBP", "JPY", "INR"]

        for base in base_currencies:
            if base not in currencies:
                continue
            for target, target_name in currencies.items():
                if target == base:
                    continue
                pairs.append({
                    "base_currency": base,
                    "target_currency": target,
                    "pair_name": f"{base}/{target}",
                    "source": "frankfurter",
                    "is_active": True
                })

        df = pd.DataFrame(pairs)
        self.logger.info("Pairs transformed", count=len(df))
        return df

    def _transform_latest(self, latest_data: Dict[str, Dict]) -> pd.DataFrame:
        rows = []

        for base_currency, data in latest_data.items():
            rate_date = self._safe_date(data.get("date"))
            rates = data.get("rates", {})

            for target_currency, rate in rates.items():
                clean_rate = self._safe_float(rate)
                if clean_rate is not None and clean_rate > 0 and rate_date is not None:
                    rows.append({
                        "base_currency": base_currency,
                        "target_currency": target_currency,
                        "rate_date": rate_date,
                        "exchange_rate": clean_rate,
                        "source": "frankfurter",
                        "raw_response_id": None
                    })

        df = pd.DataFrame(rows)
        if not df.empty:
            df = self._validate_dataframe(
                df,
                required_columns=["base_currency", "target_currency", "rate_date", "exchange_rate"]
            )
        return df

    def _transform_historical(self, historical_data: List[Dict]) -> pd.DataFrame:
        rows = []

        for entry in historical_data:
            base_currency = entry.get("_base_currency", entry.get("base", "USD"))
            raw_id = entry.get("_raw_id")
            rates_by_date = entry.get("rates", {})

            for date_str, rates in rates_by_date.items():
                rate_date = self._safe_date(date_str)
                if rate_date is None:
                    continue

                for target_currency, rate in rates.items():
                    clean_rate = self._safe_float(rate)
                    if clean_rate is not None and clean_rate > 0:
                        rows.append({
                            "base_currency": base_currency,
                            "target_currency": target_currency,
                            "rate_date": rate_date,
                            "exchange_rate": clean_rate,
                            "source": "frankfurter",
                            "raw_response_id": raw_id
                        })

        df = pd.DataFrame(rows)
        if not df.empty:
            df = self._validate_dataframe(
                df,
                required_columns=["base_currency", "target_currency", "rate_date", "exchange_rate"]
            )
            self.logger.info("Historical rates transformed", rows=len(df))
        return df
