import json
from pathlib import Path
from typing import Dict, Any, List

import pandas as pd

from config.settings import settings
from config.logging_config import get_logger

logger = get_logger("json_exporter")


def export_sample_json(
    data: pd.DataFrame,
    filename: str,
    sample_size: int = 20,
    metadata: Dict = None
) -> str:
    output_dir = settings.OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / filename

    if len(data) > sample_size:
        sample_df = data.head(sample_size).copy()
    else:
        sample_df = data.copy()

    sample_df = sample_df.where(pd.notnull(sample_df), None)
    records = sample_df.to_dict(orient="records")

    output = {
        "status": "success",
        "meta": {
            "source": metadata.get("source", "mfapis") if metadata else "mfapis",
            "total_records": len(data),
            "sample_size": len(records),
            "generated_at": pd.Timestamp.now("UTC").isoformat(),
            **(metadata or {})
        },
        "data": records
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, default=str, ensure_ascii=False)

    logger.info("JSON sample exported", file=str(filepath), records=len(records))
    return str(filepath)
