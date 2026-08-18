from __future__ import annotations

import geopandas as gpd
import pandas as pd


def filter_places(
    gdf: gpd.GeoDataFrame,
    categories: list[str] | None = None,
    min_population: int = 0,
    max_population: int | None = None,
    min_value: int = 0,
) -> gpd.GeoDataFrame:
    result = gdf.copy()
    if categories:
        result = result[result["category"].isin(categories)]
    result = result[result["population"] >= min_population]
    if max_population is not None:
        result = result[result["population"] <= max_population]
    result = result[result["value"] >= min_value]
    return result


def summary_stats(gdf: gpd.GeoDataFrame) -> dict:
    return {
        "feature_count": int(len(gdf)),
        "total_population": int(gdf["population"].sum()) if len(gdf) else 0,
        "mean_population": float(gdf["population"].mean()) if len(gdf) else 0.0,
        "mean_value": float(gdf["value"].mean()) if len(gdf) else 0.0,
        "top_category": (
            gdf["category"].value_counts().idxmax() if len(gdf) else "None"
        ),
    }


def category_summary(gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    if gdf.empty:
        return pd.DataFrame(columns=["category", "count", "population", "mean_value"])
    return (
        gdf.groupby("category")
        .agg(
            count=("id", "count"),
            population=("population", "sum"),
            mean_value=("value", "mean"),
        )
        .reset_index()
    )


def to_csv_bytes(gdf: gpd.GeoDataFrame) -> bytes:
    table = gdf.drop(columns="geometry").to_csv(index=False)
    return table.encode("utf-8")


def to_geojson_bytes(gdf: gpd.GeoDataFrame) -> bytes:
    return gdf.to_json().encode("utf-8")
