from abc import ABC, abstractmethod
from typing import Any

import pandas as pd

from config.logging_config import get_logger


class BaseTransformer(ABC):

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.errors = []

    @abstractmethod
    def transform(self, raw_data: Any) -> pd.DataFrame:
        pass

    def _validate_dataframe(self, df: pd.DataFrame, required_columns: list) -> pd.DataFrame:
        initial_count = len(df)

        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        df = df.dropna(subset=required_columns)
        df = df.drop_duplicates()

        removed = initial_count - len(df)
        if removed > 0:
            self.logger.warning(
                "Rows removed during validation",
                initial=initial_count,
                removed=removed,
                remaining=len(df)
            )

        return df

    def _safe_float(self, value: Any) -> float:
        if value is None:
            return None
        try:
            if isinstance(value, str):
                value = value.strip()
                if value in ("", ".", "N/A", "NA", "null", "None", "-"):
                    return None
            return float(value)
        except (ValueError, TypeError):
            return None

    def _safe_date(self, value: Any) -> Any:
        if value is None:
            return None
        try:
            return pd.to_datetime(value).date()
        except Exception:
            return None
