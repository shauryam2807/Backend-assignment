import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from transformers.forex_transformer import ForexTransformer
from transformers.crypto_transformer import CryptoTransformer
from transformers.economic_transformer import EconomicTransformer


class TestForexIntegration:

    def test_full_transform_flow(self, sample_forex_raw_data):
        transformer = ForexTransformer()
        result = transformer.transform(sample_forex_raw_data)
        assert "pairs" in result
        assert "daily_rates" in result
        rates_df = result["daily_rates"]
        assert all(rates_df["exchange_rate"] > 0)
        assert rates_df["base_currency"].notna().all()

    def test_transform_output_types(self, sample_forex_raw_data):
        transformer = ForexTransformer()
        result = transformer.transform(sample_forex_raw_data)
        assert isinstance(result["pairs"], pd.DataFrame)
        assert isinstance(result["daily_rates"], pd.DataFrame)

    def test_transform_pairs_unique(self, sample_forex_raw_data):
        transformer = ForexTransformer()
        result = transformer.transform(sample_forex_raw_data)
        pairs_df = result["pairs"]
        duplicates = pairs_df.duplicated(subset=["base_currency", "target_currency"])
        assert not duplicates.any()


class TestCryptoIntegration:

    def test_full_transform_flow(self, sample_crypto_raw_data):
        transformer = CryptoTransformer()
        result = transformer.transform(sample_crypto_raw_data)
        assert "coins" in result
        assert "daily_prices" in result
        assert len(result["coins"]) == 2
        assert len(result["daily_prices"]) > 0

    def test_transform_output_types(self, sample_crypto_raw_data):
        transformer = CryptoTransformer()
        result = transformer.transform(sample_crypto_raw_data)
        assert isinstance(result["coins"], pd.DataFrame)
        assert isinstance(result["daily_prices"], pd.DataFrame)

    def test_bitcoin_in_results(self, sample_crypto_raw_data):
        transformer = CryptoTransformer()
        result = transformer.transform(sample_crypto_raw_data)
        coins = result["coins"]
        assert "bitcoin" in coins["coin_id"].values


class TestEconomicIntegration:

    def test_full_transform_flow(self, sample_economic_raw_data):
        transformer = EconomicTransformer()
        result = transformer.transform(sample_economic_raw_data)
        assert "indicators" in result
        assert "values" in result
        assert len(result["indicators"]) >= 1
        assert len(result["values"]) >= 1

    def test_transform_output_types(self, sample_economic_raw_data):
        transformer = EconomicTransformer()
        result = transformer.transform(sample_economic_raw_data)
        assert isinstance(result["indicators"], pd.DataFrame)
        assert isinstance(result["values"], pd.DataFrame)

    def test_missing_values_not_in_output(self, sample_economic_raw_data):
        transformer = EconomicTransformer()
        result = transformer.transform(sample_economic_raw_data)
        values_df = result["values"]
        non_null_values = values_df["value"].dropna()
        for v in non_null_values:
            assert v != "."


class TestPipelineOrchestration:

    def test_all_transformers_accept_empty_data(self):
        forex_t = ForexTransformer()
        crypto_t = CryptoTransformer()
        economic_t = EconomicTransformer()

        forex_result = forex_t.transform({
            "currencies": {},
            "latest_rates": {},
            "historical_rates": []
        })
        assert isinstance(forex_result["pairs"], pd.DataFrame)

        crypto_result = crypto_t.transform({
            "market_data": [],
            "historical_data": {}
        })
        assert isinstance(crypto_result["coins"], pd.DataFrame)

        economic_result = economic_t.transform({"indicators": {}})
        assert isinstance(economic_result["indicators"], pd.DataFrame)

    def test_transformer_output_consistency(self, sample_forex_raw_data, sample_crypto_raw_data, sample_economic_raw_data):
        forex_result = ForexTransformer().transform(sample_forex_raw_data)
        crypto_result = CryptoTransformer().transform(sample_crypto_raw_data)
        economic_result = EconomicTransformer().transform(sample_economic_raw_data)

        assert len(forex_result) == 2
        assert len(crypto_result) == 2
        assert len(economic_result) == 2

        for result in [forex_result, crypto_result, economic_result]:
            for key, df in result.items():
                assert isinstance(df, pd.DataFrame)
