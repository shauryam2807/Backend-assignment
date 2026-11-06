from datetime import datetime, timezone
from typing import Dict, Any, List

import pandas as pd

from transformers.base_transformer import BaseTransformer


class CryptoTransformer(BaseTransformer):

    def transform(self, raw_data: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        self.logger.info("Starting Crypto data transformation")

        coins_df = self._transform_coins(raw_data.get("market_data", []))
        current_prices_df = self._transform_current_prices(raw_data.get("market_data", []))
        historical_df = self._transform_historical(raw_data.get("historical_data", {}))

        if not current_prices_df.empty and not historical_df.empty:
            daily_prices_df = pd.concat([historical_df, current_prices_df], ignore_index=True)
        elif not current_prices_df.empty:
            daily_prices_df = current_prices_df
        else:
            daily_prices_df = historical_df

        if not daily_prices_df.empty:
            daily_prices_df = daily_prices_df.drop_duplicates(
                subset=["coin_id", "price_date"],
                keep="last"
            )

        self.logger.info(
            "Crypto transformation complete",
            coins=len(coins_df),
            price_records=len(daily_prices_df)
        )

        return {
            "coins": coins_df,
            "daily_prices": daily_prices_df
        }

    def _transform_coins(self, market_data: List[Dict]) -> pd.DataFrame:
        rows = []
        for coin in market_data:
            rows.append({
                "coin_id": coin.get("id", ""),
                "symbol": coin.get("symbol", "").upper(),
                "name": coin.get("name", ""),
                "market_cap_rank": coin.get("market_cap_rank"),
                "category": "cryptocurrency",
                "description": None,
                "homepage_url": None,
                "image_url": coin.get("image"),
                "source": "coingecko",
                "is_active": True
            })

        df = pd.DataFrame(rows)
        if not df.empty:
            df = self._validate_dataframe(df, required_columns=["coin_id", "symbol", "name"])
        return df

    def _transform_current_prices(self, market_data: List[Dict]) -> pd.DataFrame:
        rows = []
        today = datetime.now(timezone.utc).date()

        for coin in market_data:
            rows.append({
                "coin_id": coin.get("id", ""),
                "price_date": today,
                "price_usd": self._safe_float(coin.get("current_price")),
                "market_cap_usd": self._safe_float(coin.get("market_cap")),
                "total_volume_usd": self._safe_float(coin.get("total_volume")),
                "price_change_24h": self._safe_float(coin.get("price_change_percentage_24h")),
                "high_24h": self._safe_float(coin.get("high_24h")),
                "low_24h": self._safe_float(coin.get("low_24h")),
                "circulating_supply": self._safe_float(coin.get("circulating_supply")),
                "source": "coingecko",
                "raw_response_id": None
            })

        df = pd.DataFrame(rows)
        if not df.empty:
            df = self._validate_dataframe(df, required_columns=["coin_id", "price_date"])
        return df

    def _transform_historical(self, historical_data: Dict[str, Any]) -> pd.DataFrame:
        rows = []

        for coin_id, data in historical_data.items():
            prices = data.get("prices", [])
            market_caps = data.get("market_caps", [])
            volumes = data.get("total_volumes", [])
            raw_id = data.get("_raw_id")

            mc_by_date = {}
            for ts_ms, val in market_caps:
                d = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).date()
                mc_by_date[d] = val

            vol_by_date = {}
            for ts_ms, val in volumes:
                d = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).date()
                vol_by_date[d] = val

            for ts_ms, price in prices:
                price_date = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).date()

                rows.append({
                    "coin_id": coin_id,
                    "price_date": price_date,
                    "price_usd": self._safe_float(price),
                    "market_cap_usd": self._safe_float(mc_by_date.get(price_date)),
                    "total_volume_usd": self._safe_float(vol_by_date.get(price_date)),
                    "price_change_24h": None,
                    "high_24h": None,
                    "low_24h": None,
                    "circulating_supply": None,
                    "source": "coingecko",
                    "raw_response_id": raw_id
                })

        df = pd.DataFrame(rows)
        if not df.empty:
            df = self._validate_dataframe(df, required_columns=["coin_id", "price_date"])
            self.logger.info("Historical crypto transformed", rows=len(df))
        return df
