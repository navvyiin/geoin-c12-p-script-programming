from __future__ import annotations

import geopandas as gpd

def generate_buffers(gdf: gpd.GeoDataFrame, distance: float, segments: int = 16) -> gpd.GeoDataFrame:
    """Generate planar buffers around vector features."""
    if gdf.crs is None:
        raise ValueError("Input layer must have a CRS.")
    out = gdf.copy()
    out["geometry"] = out.geometry.buffer(distance, resolution=segments)
    out["buffer_distance"] = distance
    return out
