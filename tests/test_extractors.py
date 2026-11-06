import pytest
from unittest.mock import patch, MagicMock
from extractors.forex_extractor import ForexExtractor
from extractors.crypto_extractor import CryptoExtractor
from extractors.economic_extractor import EconomicExtractor


class TestForexExtractor:

    def test_source_name(self):
        extractor = ForexExtractor()
        assert extractor.get_source_name() == "forex"

    def test_has_extract_method(self):
        extractor = ForexExtractor()
        assert hasattr(extractor, "extract")
        assert callable(extractor.extract)

    @patch.object(ForexExtractor, "_make_request")
    def test_extract_currencies(self, mock_request):
        mock_request.return_value = {"USD": "United States Dollar", "EUR": "Euro"}
        extractor = ForexExtractor()
        result = extractor.extract()
        assert "currencies" in result
        assert "USD" in result["currencies"]
        assert "EUR" in result["currencies"]

    @patch.object(ForexExtractor, "_make_request")
    def test_extract_returns_latest_rates(self, mock_request):
        mock_request.return_value = {
            "base": "USD",
            "date": "2026-11-01",
            "rates": {"EUR": 0.92, "GBP": 0.79}
        }
        extractor = ForexExtractor()
        result = extractor.extract()
        assert "latest_rates" in result

    @patch.object(ForexExtractor, "_make_request")
    def test_extract_returns_historical_rates(self, mock_request):
        mock_request.return_value = {
            "base": "USD",
            "start_date": "2026-10-01",
            "end_date": "2026-11-01",
            "rates": {
                "2026-10-01": {"EUR": 0.91},
                "2026-10-02": {"EUR": 0.92}
            }
        }
        extractor = ForexExtractor()
        result = extractor.extract()
        assert "historical_rates" in result

    def test_raw_dir_uses_source_name(self):
        extractor = ForexExtractor()
        assert "forex" in str(extractor.raw_dir)


class TestCryptoExtractor:

    def test_source_name(self):
        extractor = CryptoExtractor()
        assert extractor.get_source_name() == "crypto"

    def test_has_extract_method(self):
        extractor = CryptoExtractor()
        assert callable(extractor.extract)

    @patch.object(CryptoExtractor, "_make_request")
    def test_extract_market_data(self, mock_request):
        mock_request.return_value = [
            {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin", "current_price": 95000},
            {"id": "ethereum", "symbol": "eth", "name": "Ethereum", "current_price": 3200}
        ]
        extractor = CryptoExtractor()
        result = extractor.extract()
        assert "market_data" in result
        assert len(result["market_data"]) == 2

    @patch.object(CryptoExtractor, "_make_request")
    def test_extract_returns_historical(self, mock_request):
        mock_request.return_value = [
            {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin", "current_price": 95000}
        ]
        extractor = CryptoExtractor()
        result = extractor.extract()
        assert "historical_data" in result

    def test_raw_dir_uses_source_name(self):
        extractor = CryptoExtractor()
        assert "crypto" in str(extractor.raw_dir)


class TestEconomicExtractor:

    def test_source_name(self):
        extractor = EconomicExtractor()
        assert extractor.get_source_name() == "economic"

    def test_has_extract_method(self):
        extractor = EconomicExtractor()
        assert callable(extractor.extract)

    def test_raw_dir_uses_source_name(self):
        extractor = EconomicExtractor()
        assert "economic" in str(extractor.raw_dir)


class TestBaseExtractorBehavior:

    def test_all_extractors_have_save_raw(self):
        for ExtractorClass in [ForexExtractor, CryptoExtractor, EconomicExtractor]:
            extractor = ExtractorClass()
            assert hasattr(extractor, "_save_raw_response")

    def test_all_extractors_have_make_request(self):
        for ExtractorClass in [ForexExtractor, CryptoExtractor, EconomicExtractor]:
            extractor = ExtractorClass()
            assert hasattr(extractor, "_make_request")

    def test_all_extractors_have_logger(self):
        for ExtractorClass in [ForexExtractor, CryptoExtractor, EconomicExtractor]:
            extractor = ExtractorClass()
            assert hasattr(extractor, "logger")

    def test_all_extractors_have_raw_dir(self):
        for ExtractorClass in [ForexExtractor, CryptoExtractor, EconomicExtractor]:
            extractor = ExtractorClass()
            assert hasattr(extractor, "raw_dir")

    def test_source_names_are_unique(self):
        names = set()
        for ExtractorClass in [ForexExtractor, CryptoExtractor, EconomicExtractor]:
            name = ExtractorClass().get_source_name()
            assert name not in names
            names.add(name)
