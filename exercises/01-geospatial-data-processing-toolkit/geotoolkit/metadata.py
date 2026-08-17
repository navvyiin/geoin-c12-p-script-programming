from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import geopandas as gpd
import rasterio


def vector_metadata(gdf: gpd.GeoDataFrame, source: str | None = None) -> dict[str, Any]:
    bounds = tuple(float(x) for x in gdf.total_bounds) if not gdf.empty else None
    geom_counts = gdf.geometry.geom_type.value_counts().to_dict() if "geometry" in gdf else {}
    return {
        "dataset_type": "vector",
        "source": str(source) if source else None,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "feature_count": int(len(gdf)),
        "columns": [str(c) for c in gdf.columns],
        "crs": gdf.crs.to_string() if gdf.crs else None,
        "bounds": bounds,
        "geometry_types": geom_counts,
    }


def raster_metadata(path: str | Path) -> dict[str, Any]:
    with rasterio.open(path) as src:
        return {
            "dataset_type": "raster",
            "source": str(path),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "width": src.width,
            "height": src.height,
            "bands": src.count,
            "dtype": str(src.dtypes[0]) if src.count else None,
            "crs": src.crs.to_string() if src.crs else None,
            "bounds": tuple(float(v) for v in src.bounds),
            "transform": tuple(float(v) for v in src.transform),
            "nodata": src.nodata,
        }
