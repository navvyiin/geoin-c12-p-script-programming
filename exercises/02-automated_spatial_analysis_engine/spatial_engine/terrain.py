from __future__ import annotations

from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import Affine


def slope_aspect(dem_path: str | Path, slope_out: str | Path, aspect_out: str | Path) -> dict:
    """Create slope and aspect rasters from a DEM."""
    with rasterio.open(dem_path) as src:
        arr = src.read(1, masked=True).filled(np.nan).astype(float)
        transform = src.transform
        dx = abs(transform.a)
        dy = abs(transform.e)
        gy, gx = np.gradient(arr, dy, dx)
        slope = np.degrees(np.arctan(np.sqrt(gx ** 2 + gy ** 2)))
        aspect = (np.degrees(np.arctan2(-gx, gy)) + 360.0) % 360.0
        profile = src.profile.copy()
        profile.update(dtype="float32", count=1, nodata=-9999.0)
        for target, data in [(slope_out, slope), (aspect_out, aspect)]:
            out = np.where(np.isfinite(data), data, -9999.0).astype("float32")
            with rasterio.open(target, "w", **profile) as dst:
                dst.write(out, 1)
    return {"slope": str(slope_out), "aspect": str(aspect_out)}
