from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path


def configure_logging(log_path: str | Path | None = None, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger("geotoolkit")
    logger.setLevel(level)
    if logger.handlers:
        return logger
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)
    if log_path:
        path = Path(log_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(path, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(file_handler)
    return logger


def write_processing_log(records: list[dict], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "operations": records,
    }
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
