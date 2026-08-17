from __future__ import annotations

from pathlib import Path
from typing import Sequence

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
from shapely.geometry import mapping


def validate_crs(obj, expected: str | None = None) -> dict:
    """Validate that a dataset has a CRS and optionally compare it to an expected CRS."""
    crs = getattr(obj, "crs", None)
    result = {"has_crs": crs is not None, "crs": crs.to_string() if crs else None, "matches_expected": None}
    if crs is None:
        return result
    if expected:
        result["matches_expected"] = crs == expected or crs.equals(expected)
    return result


def reproject_vector(gdf: gpd.GeoDataFrame, target_crs: str) -> gpd.GeoDataFrame:
    if gdf.crs is None:
        raise ValueError("Input vector has no CRS. Assign a CRS before reprojection.")
    return gdf.to_crs(target_crs)


def reproject_raster(src_path: str | Path, dst_path: str | Path, target_crs: str, resampling=Resampling.nearest) -> Path:
    dst_path = Path(dst_path)
    with rasterio.open(src_path) as src:
        if src.crs is None:
            raise ValueError("Input raster has no CRS.")
        transform, width, height = calculate_default_transform(src.crs, target_crs, src.width, src.height, *src.bounds)
        profile = src.profile.copy()
        profile.update(crs=target_crs, transform=transform, width=width, height=height)
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(dst_path, "w", **profile) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=target_crs,
                    resampling=resampling,
                )
    return dst_path


def clip_vector(gdf: gpd.GeoDataFrame, mask_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if gdf.crs is None or mask_gdf.crs is None:
        raise ValueError("Both vector and mask layers must have a CRS before clipping.")
    if gdf.crs != mask_gdf.crs:
        mask_gdf = mask_gdf.to_crs(gdf.crs)
    return gpd.clip(gdf, mask_gdf)


def clip_raster(src_path: str | Path, mask_gdf: gpd.GeoDataFrame, dst_path: str | Path, crop: bool = True) -> Path:
    dst_path = Path(dst_path)
    with rasterio.open(src_path) as src:
        if mask_gdf.crs is None:
            raise ValueError("Raster mask layer has no CRS.")
        if src.crs is None:
            raise ValueError("Input raster has no CRS.")
        if mask_gdf.crs != src.crs:
            mask_gdf = mask_gdf.to_crs(src.crs)
        shapes = [mapping(geom) for geom in mask_gdf.geometry if geom is not None and not geom.is_empty]
        out_image, out_transform = mask(src, shapes, crop=crop)
        profile = src.profile.copy()
        profile.update(height=out_image.shape[1], width=out_image.shape[2], transform=out_transform)
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(dst_path, "w", **profile) as dst:
            dst.write(out_image)
    return dst_path


def merge_vectors(gdfs: Sequence[gpd.GeoDataFrame]) -> gpd.GeoDataFrame:
    if not gdfs:
        raise ValueError("At least one vector layer is required.")
    base_crs = gdfs[0].crs
    aligned = []
    for gdf in gdfs:
        if gdf.crs != base_crs:
            gdf = gdf.to_crs(base_crs)
        aligned.append(gdf)
    return gpd.GeoDataFrame(pd.concat(aligned, ignore_index=True), crs=base_crs)


def merge_rasters(src_paths: Sequence[str | Path], dst_path: str | Path) -> Path:
    from rasterio.merge import merge

    srcs = [rasterio.open(p) for p in src_paths]
    try:
        if not srcs:
            raise ValueError("At least one raster is required.")
        mosaic, transform = merge(srcs)
        profile = srcs[0].profile.copy()
        profile.update(height=mosaic.shape[1], width=mosaic.shape[2], transform=transform)
        dst_path = Path(dst_path)
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(dst_path, "w", **profile) as dst:
            dst.write(mosaic)
        return dst_path
    finally:
        for src in srcs:
            src.close()
