from __future__ import annotations

from pathlib import Path
import geopandas as gpd
from shapely.geometry import Point, Polygon


def create_sample_data(output_dir: str | Path) -> dict[str, Path]:
    """Create small deterministic vector layers for the dashboard."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    places = gpd.GeoDataFrame(
        {
            "id": [1, 2, 3, 4, 5, 6],
            "name": ["Central Hub", "North Gate", "South Park", "East Market", "West End", "Lakeside"],
            "population": [12000, 8500, 6400, 9100, 5300, 7200],
            "category": ["Urban", "Urban", "Park", "Commercial", "Rural", "Park"],
            "value": [82, 71, 65, 91, 48, 76],
        },
        geometry=[
            Point(77.590, 12.970),
            Point(77.585, 13.010),
            Point(77.575, 12.925),
            Point(77.615, 12.970),
            Point(77.520, 12.965),
            Point(77.555, 12.960),
        ],
        crs="EPSG:4326",
    )

    zones = gpd.GeoDataFrame(
        {
            "zone_id": [101, 102, 103],
            "zone_name": ["Central Zone", "North Zone", "South Zone"],
            "priority": [3, 2, 1],
            "score": [88, 72, 61],
        },
        geometry=[
            Polygon([(77.54, 12.94), (77.62, 12.94), (77.62, 13.00), (77.54, 13.00)]),
            Polygon([(77.54, 13.00), (77.63, 13.00), (77.63, 13.05), (77.54, 13.05)]),
            Polygon([(77.54, 12.89), (77.63, 12.89), (77.63, 12.94), (77.54, 12.94)]),
        ],
        crs="EPSG:4326",
    )

    places_path = output_dir / "places.geojson"
    zones_path = output_dir / "zones.geojson"
    places.to_file(places_path, driver="GeoJSON")
    zones.to_file(zones_path, driver="GeoJSON")
    return {"places": places_path, "zones": zones_path}


def load_layers(data_dir: str | Path) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    data_dir = Path(data_dir)
    places_path = data_dir / "places.geojson"
    zones_path = data_dir / "zones.geojson"
    if not places_path.exists() or not zones_path.exists():
        create_sample_data(data_dir)
    return gpd.read_file(places_path), gpd.read_file(zones_path)
