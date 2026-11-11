from datetime import datetime, timezone
from typing import Dict, Any, List
import pandas as pd
from transformers.base_transformer import BaseTransformer


class BinanceTransformer(BaseTransformer):
    """
    Transforms Binance kline candles into Twelve Data compatible OHLCV structures.
    """

    SYMBOL_NORMALIZATION = {
        "BTCUSDT": "BTC/USD",
        "ETHUSDT": "ETH/USD",
        "SOLUSDT": "SOL/USD",
        "BNBUSDT": "BNB/USD",
        "XRPUSDT": "XRP/USD"
    }

    def transform(self, raw_data: Dict[str, Any]) -> pd.DataFrame:
        self.logger.info("Starting Binance OHLCV transformation")
        rows = []

        for sym, entry in raw_data.items():
            klines = entry.get("klines", [])
            raw_id = entry.get("raw_id")
            normalized_sym = self.SYMBOL_NORMALIZATION.get(sym, sym)

            for candle in klines:
                if len(candle) < 6:
                    continue

                open_time_ms = candle[0]
                candle_date = datetime.fromtimestamp(open_time_ms / 1000, tz=timezone.utc).date()

                open_p = self._safe_float(candle[1])
                high_p = self._safe_float(candle[2])
                low_p = self._safe_float(candle[3])
                close_p = self._safe_float(candle[4])
                vol = self._safe_float(candle[5])
                quote_vol = self._safe_float(candle[7]) if len(candle) > 7 else 0.0

                if all(v is not None for v in [open_p, high_p, low_p, close_p]) and candle_date:
                    rows.append({
                        "symbol": normalized_sym,
                        "candle_date": candle_date,
                        "open_price": open_p,
                        "high_price": high_p,
                        "low_price": low_p,
                        "close_price": close_p,
                        "volume": vol or 0.0,
                        "quote_volume": quote_vol or 0.0,
                        "source": "binance",
                        "raw_response_id": raw_id
                    })

        df = pd.DataFrame(rows)
        if not df.empty:
            df = df.drop_duplicates(subset=["symbol", "candle_date"], keep="last")
            df = self._validate_dataframe(
                df,
                required_columns=["symbol", "candle_date", "open_price", "high_price", "low_price", "close_price"]
            )
            self.logger.info("Binance OHLCV transformed", total_candles=len(df), symbols=df["symbol"].nunique())

        return df

