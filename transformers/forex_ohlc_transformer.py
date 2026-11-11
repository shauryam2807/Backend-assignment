from datetime import datetime, timezone
from typing import Dict, Any, List
import pandas as pd
from transformers.base_transformer import BaseTransformer


class ForexOHLCTransformer(BaseTransformer):
    """
    Transforms institutional Forex chart candles into Twelve Data compatible OHLCV structures.
    """

    def transform(self, raw_data: Dict[str, Any]) -> pd.DataFrame:
        self.logger.info("Starting Forex OHLC transformation")
        rows = []

        for pair, entry in raw_data.items():
            chart = entry.get("chart", {})
            raw_id = entry.get("raw_id")

            result_list = chart.get("chart", {}).get("result", [])
            if not result_list:
                continue

            result = result_list[0]
            timestamps = result.get("timestamp", [])
            indicators = result.get("indicators", {})
            quote_list = indicators.get("quote", [])

            if not quote_list or not timestamps:
                continue

            quote = quote_list[0]
            opens = quote.get("open", [])
            highs = quote.get("high", [])
            lows = quote.get("low", [])
            closes = quote.get("close", [])
            volumes = quote.get("volume", [])

            parts = pair.split("/")
            base = parts[0] if len(parts) > 0 else "EUR"
            target = parts[1] if len(parts) > 1 else "USD"

            for i in range(len(timestamps)):
                ts = timestamps[i]
                if ts is None:
                    continue

                candle_date = datetime.fromtimestamp(ts, tz=timezone.utc).date()

                o = self._safe_float(opens[i]) if i < len(opens) else None
                h = self._safe_float(highs[i]) if i < len(highs) else None
                l = self._safe_float(lows[i]) if i < len(lows) else None
                c = self._safe_float(closes[i]) if i < len(closes) else None
                v = self._safe_float(volumes[i]) if i < len(volumes) else 0.0

                if all(val is not None for val in [o, h, l, c]) and candle_date:
                    rows.append({
                        "pair_name": pair,
                        "base_currency": base,
                        "target_currency": target,
                        "candle_date": candle_date,
                        "open_price": o,
                        "high_price": h,
                        "low_price": l,
                        "close_price": c,
                        "volume": v or 0.0,
                        "source": "yahoo_finance",
                        "raw_response_id": raw_id
                    })

        df = pd.DataFrame(rows)
        if not df.empty:
            df = df.drop_duplicates(subset=["pair_name", "candle_date"], keep="last")
            df = self._validate_dataframe(
                df,
                required_columns=["pair_name", "candle_date", "open_price", "high_price", "low_price", "close_price"]
            )
            self.logger.info("Forex OHLC transformed", total_candles=len(df), pairs=df["pair_name"].nunique())

        return df

