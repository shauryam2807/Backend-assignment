import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from extractors.binance_extractor import BinanceExtractor
from extractors.forex_ohlc_extractor import ForexOHLCExtractor
from transformers.binance_transformer import BinanceTransformer
from transformers.forex_ohlc_transformer import ForexOHLCTransformer


class TestBinanceExtractor:
    def test_source_name(self):
        extractor = BinanceExtractor()
        assert extractor.get_source_name() == "crypto"

    @patch.object(BinanceExtractor, "_make_request")
    def test_extract_klines(self, mock_req):
        mock_req.return_value = [
            [1700000000000, "90000.0", "91000.0", "89000.0", "90500.0", "100.0", 1700086400000, "9050000.0"]
        ]
        extractor = BinanceExtractor()
        data = extractor.extract(symbols=["BTCUSDT"])
        assert "BTCUSDT" in data
        assert len(data["BTCUSDT"]["klines"]) == 1


class TestForexOHLCExtractor:
    def test_source_name(self):
        extractor = ForexOHLCExtractor()
        assert extractor.get_source_name() == "forex"

    @patch.object(ForexOHLCExtractor, "_make_request")
    def test_extract_forex_chart(self, mock_req):
        mock_req.return_value = {
            "chart": {
                "result": [{
                    "timestamp": [1700000000],
                    "indicators": {"quote": [{"open": [1.08], "high": [1.09], "low": [1.07], "close": [1.085], "volume": [0]}]}
                }]
            }
        }
        extractor = ForexOHLCExtractor()
        data = extractor.extract(pairs=["EUR/USD"])
        assert "EUR/USD" in data
        assert "chart" in data["EUR/USD"]


class TestBinanceTransformer:
    def test_transform_valid_klines(self):
        transformer = BinanceTransformer()
        raw = {
            "BTCUSDT": {
                "raw_id": "test_id",
                "klines": [
                    [1700000000000, "90000.0", "91000.0", "89000.0", "90500.0", "100.5", 1700086400000, "9050000.0"]
                ]
            }
        }
        df = transformer.transform(raw)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert df["symbol"].iloc[0] == "BTC/USD"
        assert df["open_price"].iloc[0] == 90000.0
        assert df["close_price"].iloc[0] == 90500.0


class TestForexOHLCTransformer:
    def test_transform_valid_chart(self):
        transformer = ForexOHLCTransformer()
        raw = {
            "EUR/USD": {
                "raw_id": "test_id",
                "chart": {
                    "chart": {
                        "result": [{
                            "timestamp": [1700000000],
                            "indicators": {
                                "quote": [{
                                    "open": [1.0850],
                                    "high": [1.0920],
                                    "low": [1.0810],
                                    "close": [1.0890],
                                    "volume": [0]
                                }]
                            }
                        }]
                    }
                }
            }
        }
        df = transformer.transform(raw)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert df["pair_name"].iloc[0] == "EUR/USD"
        assert df["open_price"].iloc[0] == 1.0850
        assert df["close_price"].iloc[0] == 1.0890

