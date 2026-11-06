import pytest
import pandas as pd
from datetime import date

from transformers.forex_transformer import ForexTransformer
from transformers.crypto_transformer import CryptoTransformer
from transformers.economic_transformer import EconomicTransformer
from transformers.base_transformer import BaseTransformer


class TestForexTransformer:

    def setup_method(self):
        self.transformer = ForexTransformer()

    def test_transform_produces_pairs_and_rates(self, sample_forex_raw_data):
        result = self.transformer.transform(sample_forex_raw_data)
        assert "pairs" in result
        assert "daily_rates" in result
        assert isinstance(result["pairs"], pd.DataFrame)
        assert isinstance(result["daily_rates"], pd.DataFrame)

    def test_pairs_have_correct_columns(self, sample_forex_raw_data):
        result = self.transformer.transform(sample_forex_raw_data)
        pairs = result["pairs"]
        required_columns = ["base_currency", "target_currency", "pair_name", "source"]
        for col in required_columns:
            assert col in pairs.columns

    def test_rates_have_correct_columns(self, sample_forex_raw_data):
        result = self.transformer.transform(sample_forex_raw_data)
        rates = result["daily_rates"]
        required_columns = [
            "base_currency", "target_currency",
            "rate_date", "exchange_rate", "source"
        ]
        for col in required_columns:
            assert col in rates.columns

    def test_no_duplicate_rates(self, sample_forex_raw_data):
        result = self.transformer.transform(sample_forex_raw_data)
        rates = result["daily_rates"]
        if not rates.empty:
            duplicates = rates.duplicated(
                subset=["base_currency", "target_currency", "rate_date"]
            )
            assert not duplicates.any()

    def test_rates_are_positive(self, sample_forex_raw_data):
        result = self.transformer.transform(sample_forex_raw_data)
        rates = result["daily_rates"]
        if not rates.empty:
            assert (rates["exchange_rate"] > 0).all()

    def test_handles_empty_input(self):
        result = self.transformer.transform({
            "currencies": {},
            "latest_rates": {},
            "historical_rates": []
        })
        assert result["pairs"].empty or len(result["pairs"]) == 0
        assert result["daily_rates"].empty or len(result["daily_rates"]) == 0


class TestCryptoTransformer:

    def setup_method(self):
        self.transformer = CryptoTransformer()

    def test_transform_produces_coins_and_prices(self, sample_crypto_raw_data):
        result = self.transformer.transform(sample_crypto_raw_data)
        assert "coins" in result
        assert "daily_prices" in result

    def test_coins_have_required_fields(self, sample_crypto_raw_data):
        result = self.transformer.transform(sample_crypto_raw_data)
        coins = result["coins"]
        assert "coin_id" in coins.columns
        assert "symbol" in coins.columns
        assert "name" in coins.columns
        assert len(coins) == 2

    def test_historical_timestamps_converted(self, sample_crypto_raw_data):
        result = self.transformer.transform(sample_crypto_raw_data)
        prices = result["daily_prices"]
        assert len(prices) > 0
        btc_prices = prices[prices["coin_id"] == "bitcoin"]
        assert len(btc_prices) > 0

    def test_symbol_uppercase(self, sample_crypto_raw_data):
        result = self.transformer.transform(sample_crypto_raw_data)
        coins = result["coins"]
        assert (coins["symbol"] == coins["symbol"].str.upper()).all()


class TestEconomicTransformer:

    def setup_method(self):
        self.transformer = EconomicTransformer()

    def test_transform_produces_indicators_and_values(self, sample_economic_raw_data):
        result = self.transformer.transform(sample_economic_raw_data)
        assert "indicators" in result
        assert "values" in result

    def test_missing_values_handled(self, sample_economic_raw_data):
        result = self.transformer.transform(sample_economic_raw_data)
        values = result["values"]
        assert len(values) == 4

    def test_indicator_metadata_extracted(self, sample_economic_raw_data):
        result = self.transformer.transform(sample_economic_raw_data)
        indicators = result["indicators"]
        assert len(indicators) == 1
        assert indicators.iloc[0]["indicator_id"] == "GDP"
        assert "Gross Domestic Product" in indicators.iloc[0]["name"]


class TestBaseTransformerHelpers:

    class ConcreteTransformer(BaseTransformer):
        def transform(self, raw_data):
            return pd.DataFrame()

    def setup_method(self):
        self.transformer = self.ConcreteTransformer()

    def test_safe_float_normal(self):
        assert self.transformer._safe_float("123.45") == 123.45
        assert self.transformer._safe_float(42) == 42.0
        assert self.transformer._safe_float(0) == 0.0

    def test_safe_float_missing_values(self):
        assert self.transformer._safe_float(None) is None
        assert self.transformer._safe_float("") is None
        assert self.transformer._safe_float(".") is None
        assert self.transformer._safe_float("N/A") is None
        assert self.transformer._safe_float("null") is None

    def test_safe_float_invalid(self):
        assert self.transformer._safe_float("abc") is None
        assert self.transformer._safe_float("not_a_number") is None

    def test_safe_date_valid(self):
        result = self.transformer._safe_date("2026-10-30")
        assert result == date(2026, 10, 30)

    def test_safe_date_invalid(self):
        assert self.transformer._safe_date("not-a-date") is None
        assert self.transformer._safe_date(None) is None
