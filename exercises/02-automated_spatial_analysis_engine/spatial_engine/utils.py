from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import geopandas as gpd


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def setup_logger(path: str | Path) -> logging.Logger:
    logger = logging.getLogger("spatial_engine")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    handler = logging.FileHandler(path, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def save_json(data: Any, path: str | Path) -> None:
    Path(path).write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def write_vector(gdf: gpd.GeoDataFrame, path: str | Path) -> None:
    path = Path(path)
    ensure_dir(path.parent)
    ext = path.suffix.lower()
    if ext == ".gpkg":
        gdf.to_file(path, driver="GPKG")
    elif ext == ".geojson":
        gdf.to_file(path, driver="GeoJSON")
    elif ext == ".parquet":
        gdf.to_parquet(path, index=False)
    else:
        gdf.to_file(path)
