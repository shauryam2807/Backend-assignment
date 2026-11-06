import json
import os
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config.settings import settings
from config.logging_config import get_logger


class BaseExtractor(ABC):

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.raw_dir = settings.RAW_RESPONSES_DIR / self.get_source_name()
        self.raw_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def get_source_name(self) -> str:
        pass

    @abstractmethod
    def extract(self) -> Any:
        pass

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((requests.ConnectionError, requests.Timeout)),
        reraise=True
    )
    def _make_request(
        self,
        url: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict:
        self.logger.info("Making HTTP request", url=url, params=params)

        response = requests.get(
            url,
            params=params,
            headers=headers or {},
            timeout=settings.REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        self.logger.info(
            "Request successful",
            url=url,
            status_code=response.status_code,
            response_size=len(response.content)
        )

        return data

    def _save_raw_response(self, data: Any, filename_prefix: str) -> str:
        raw_id = self._generate_raw_id(filename_prefix)
        filepath = self.raw_dir / f"{raw_id}.json"

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str, ensure_ascii=False)

        self.logger.info("Raw response saved", file=str(filepath), raw_id=raw_id)
        return raw_id

    def _generate_raw_id(self, prefix: str) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}"
