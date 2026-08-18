from __future__ import annotations

import geopandas as gpd

def intersection(left: gpd.GeoDataFrame, right: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    return gpd.overlay(left, right, how="intersection")

def union(left: gpd.GeoDataFrame, right: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    return gpd.overlay(left, right, how="union")

def difference(left: gpd.GeoDataFrame, right: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    return gpd.overlay(left, right, how="difference")
