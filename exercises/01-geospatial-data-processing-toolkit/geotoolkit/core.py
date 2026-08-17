from __future__ import annotations

from pathlib import Path
from typing import Iterable

import geopandas as gpd

from .io import detect_type, read_vector, write_vector
from .logging_utils import configure_logging, write_processing_log
from .metadata import vector_metadata, raster_metadata
from .operations import (
    clip_raster,
    clip_vector,
    merge_rasters,
    merge_vectors,
    reproject_raster,
    reproject_vector,
    validate_crs,
)


class GeoProcessor:
    """High-level API for common vector/raster workflows."""

    def __init__(self, log_path: str | Path | None = "logs/processing.log"):
        self.logger = configure_logging(log_path)
        self.records: list[dict] = []

    def _record(self, operation: str, **kwargs):
        self.records.append({"operation": operation, **kwargs})
        self.logger.info("%s | %s", operation, kwargs)

    def save_log(self, path: str | Path = "logs/processing.json"):
        write_processing_log(self.records, path)

    def read_vector(self, path: str | Path, layer: str | None = None) -> gpd.GeoDataFrame:
        gdf = read_vector(path, layer=layer)
        self._record("read_vector", path=str(path), features=len(gdf), crs=gdf.crs.to_string() if gdf.crs else None)
        return gdf

    def validate_crs(self, obj, expected: str | None = None) -> dict:
        result = validate_crs(obj, expected)
        self._record("validate_crs", result=result)
        return result

    def reproject_vector(self, gdf: gpd.GeoDataFrame, target_crs: str) -> gpd.GeoDataFrame:
        out = reproject_vector(gdf, target_crs)
        self._record("reproject_vector", target_crs=target_crs, features=len(out))
        return out

    def clip_vector(self, gdf: gpd.GeoDataFrame, mask_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        out = clip_vector(gdf, mask_gdf)
        self._record("clip_vector", input_features=len(gdf), output_features=len(out))
        return out

    def merge_vectors(self, gdfs: Iterable[gpd.GeoDataFrame]) -> gpd.GeoDataFrame:
        gdfs = list(gdfs)
        out = merge_vectors(gdfs)
        self._record("merge_vectors", input_layers=len(gdfs), output_features=len(out))
        return out

    def export_vector(self, gdf: gpd.GeoDataFrame, path: str | Path, layer: str | None = None):
        write_vector(gdf, path, layer=layer)
        self._record("export_vector", path=str(path), metadata=vector_metadata(gdf, source=path))

    def reproject_raster(self, src_path, dst_path, target_crs):
        out = reproject_raster(src_path, dst_path, target_crs)
        self._record("reproject_raster", source=str(src_path), output=str(out), target_crs=target_crs)
        return out

    def clip_raster(self, src_path, mask_gdf, dst_path):
        out = clip_raster(src_path, mask_gdf, dst_path)
        self._record("clip_raster", source=str(src_path), output=str(out))
        return out

    def merge_rasters(self, src_paths, dst_path):
        out = merge_rasters(src_paths, dst_path)
        self._record("merge_rasters", input_count=len(src_paths), output=str(out))
        return out

    @staticmethod
    def metadata(path: str | Path) -> dict:
        kind = detect_type(path)
        if kind == "vector":
            return vector_metadata(read_vector(path), source=path)
        return raster_metadata(path)
