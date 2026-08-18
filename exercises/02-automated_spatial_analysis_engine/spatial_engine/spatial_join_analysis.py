from __future__ import annotations

import geopandas as gpd

def spatial_join(points: gpd.GeoDataFrame, polygons: gpd.GeoDataFrame, predicate: str = "within") -> gpd.GeoDataFrame:
    """Join polygon attributes to points using a spatial predicate."""
    return gpd.sjoin(points, polygons, how="left", predicate=predicate)
