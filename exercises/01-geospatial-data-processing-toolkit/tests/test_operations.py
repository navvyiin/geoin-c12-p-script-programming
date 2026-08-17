import geopandas as gpd
from shapely.geometry import Point, Polygon

from geotoolkit.operations import clip_vector, merge_vectors, reproject_vector, validate_crs


def sample():
    return gpd.GeoDataFrame({"id": [1, 2], "geometry": [Point(0, 0), Point(2, 2)]}, crs="EPSG:4326")


def test_validate_crs():
    gdf = sample()
    result = validate_crs(gdf, "EPSG:4326")
    assert result["has_crs"]
    assert result["matches_expected"] is True


def test_reproject_vector():
    out = reproject_vector(sample(), "EPSG:3857")
    assert out.crs.to_epsg() == 3857


def test_clip_vector():
    gdf = sample()
    mask = gpd.GeoDataFrame(geometry=[Polygon([(-1,-1),(1,-1),(1,1),(-1,1)])], crs="EPSG:4326")
    out = clip_vector(gdf, mask)
    assert len(out) == 1
    assert out.iloc[0]["id"] == 1


def test_merge_vectors():
    a = sample().iloc[[0]].copy()
    b = sample().iloc[[1]].copy()
    out = merge_vectors([a,b])
    assert len(out) == 2
