"""Raster input/output helpers."""
from __future__ import annotations
from pathlib import Path
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import calculate_default_transform, reproject

def read_multispectral(path):
    """Read the first four bands as blue, green, red and NIR."""
    path = Path(path)
    with rasterio.open(path) as src:
        if src.count < 4:
            raise ValueError("Expected at least four bands: blue, green, red, nir.")
        arrays = {"blue": src.read(1), "green": src.read(2), "red": src.read(3), "nir": src.read(4)}
        profile = src.profile.copy()
    return profile, arrays

def write_raster(path, array, profile, dtype="float32", nodata=-9999.0):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    out_profile = profile.copy()
    out_profile.update(count=1, dtype=dtype, nodata=nodata, compress="deflate")
    with rasterio.open(path, "w", **out_profile) as dst:
        dst.write(array.astype(dtype), 1)

def reproject_single_band(src_path, dst_path, target_crs):
    src_path, dst_path = Path(src_path), Path(dst_path)
    with rasterio.open(src_path) as src:
        transform, width, height = calculate_default_transform(src.crs, target_crs, src.width, src.height, *src.bounds)
        profile = src.profile.copy()
        profile.update(crs=target_crs, transform=transform, width=width, height=height)
        with rasterio.open(dst_path, "w", **profile) as dst:
            reproject(source=rasterio.band(src, 1), destination=rasterio.band(dst, 1), src_transform=src.transform, src_crs=src.crs, dst_transform=transform, dst_crs=target_crs, resampling=Resampling.nearest)
