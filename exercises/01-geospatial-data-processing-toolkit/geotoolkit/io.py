from __future__ import annotations

from pathlib import Path
from typing import Any

import geopandas as gpd
import rasterio
from rasterio.io import DatasetReader

VECTOR_EXTENSIONS = {".shp", ".gpkg", ".geojson", ".json", ".parquet", ".fgb"}
RASTER_EXTENSIONS = {".tif", ".tiff", ".img"}


def detect_type(path: str | Path) -> str:
    ext = Path(path).suffix.lower()
    if ext in VECTOR_EXTENSIONS:
        return "vector"
    if ext in RASTER_EXTENSIONS:
        return "raster"
    raise ValueError(f"Unsupported dataset extension: {ext}")


def read_vector(path: str | Path, layer: str | None = None, **kwargs: Any) -> gpd.GeoDataFrame:
    return gpd.read_file(path, layer=layer, **kwargs)


def read_raster(path: str | Path) -> DatasetReader:
    return rasterio.open(path)


def write_vector(gdf: gpd.GeoDataFrame, path: str | Path, layer: str | None = None, **kwargs: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        gdf.to_parquet(path, index=False)
    else:
        driver = {".gpkg": "GPKG", ".geojson": "GeoJSON", ".json": "GeoJSON", ".shp": "ESRI Shapefile", ".fgb": "FlatGeobuf"}.get(suffix)
        if not driver:
            raise ValueError(f"Cannot infer vector driver from {suffix}")
        gdf.to_file(path, driver=driver, layer=layer, **kwargs)


def write_raster(src: DatasetReader, path: str | Path, data=None, profile_updates: dict | None = None) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    profile = src.profile.copy()
    profile.update(profile_updates or {})
    with rasterio.open(path, "w", **profile) as dst:
        if data is None:
            for i in range(1, src.count + 1):
                dst.write(src.read(i), i)
        else:
            dst.write(data)
