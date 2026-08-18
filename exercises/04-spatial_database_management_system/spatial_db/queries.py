from __future__ import annotations

import geopandas as gpd


def attribute_filter(gdf: gpd.GeoDataFrame, column: str, operator: str, value) -> gpd.GeoDataFrame:
    """Filter records by an attribute expression."""
    if column not in gdf.columns:
        raise KeyError(f"Unknown field: {column}")

    if operator == "==":
        mask = gdf[column] == value
    elif operator == "!=":
        mask = gdf[column] != value
    elif operator == ">":
        mask = gdf[column] > value
    elif operator == ">=":
        mask = gdf[column] >= value
    elif operator == "<":
        mask = gdf[column] < value
    elif operator == "<=":
        mask = gdf[column] <= value
    else:
        raise ValueError("Operator must be one of ==, !=, >, >=, <, <=")
    return gdf.loc[mask].copy()


def spatial_intersection(
    features: gpd.GeoDataFrame, mask: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """Return features that intersect the mask geometry."""
    if features.crs != mask.crs:
        mask = mask.to_crs(features.crs)
    mask_geom = mask.geometry.union_all()
    return features.loc[features.geometry.intersects(mask_geom)].copy()


def spatial_within(
    features: gpd.GeoDataFrame, mask: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """Return features whose geometry lies within the mask."""
    if features.crs != mask.crs:
        mask = mask.to_crs(features.crs)
    mask_geom = mask.geometry.union_all()
    return features.loc[features.geometry.within(mask_geom)].copy()


def nearest_distance(
    points: gpd.GeoDataFrame, targets: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """Add distance to the nearest target geometry in metres."""
    if points.crs is None:
        raise ValueError("Points layer must have a CRS.")
    if targets.crs is None:
        raise ValueError("Targets layer must have a CRS.")
    if points.crs.is_geographic:
        projected_crs = points.estimate_utm_crs()
        if projected_crs is None:
            raise ValueError("Could not determine a suitable projected CRS.")
        points_projected = points.to_crs(projected_crs)
        targets_projected = targets.to_crs(projected_crs)
    else:
        points_projected = points
        targets_projected = targets.to_crs(points.crs)
    target_geom = targets_projected.geometry.union_all()
    result = points.copy()
    result["nearest_distance_m"] = points_projected.geometry.distance(target_geom)
    return result