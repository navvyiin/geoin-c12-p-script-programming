from pathlib import Path
import geopandas as gpd
from shapely.geometry import Point, Polygon


def create():
    root = Path(__file__).resolve().parents[1]
    out = root / "sample_data"
    out.mkdir(exist_ok=True)

    places = gpd.GeoDataFrame(
        {
            "place_id": [1, 2, 3, 4, 5],
            "name": ["Central", "North", "South", "East", "West"],
            "population": [12000, 8500, 6400, 9100, 5300],
            "category": ["Urban", "Urban", "Suburban", "Urban", "Rural"],
        },
        geometry=[
            Point(77.590, 12.970),
            Point(77.585, 13.010),
            Point(77.575, 12.925),
            Point(77.615, 12.970),
            Point(77.520, 12.965),
        ],
        crs="EPSG:4326",
    )

    zones = gpd.GeoDataFrame(
        {
            "zone_id": [101, 102, 103],
            "zone_name": ["Central Zone", "North Zone", "South Zone"],
            "priority": [3, 2, 1],
        },
        geometry=[
            Polygon([(77.54,12.94),(77.62,12.94),(77.62,13.00),(77.54,13.00)]),
            Polygon([(77.54,13.00),(77.63,13.00),(77.63,13.05),(77.54,13.05)]),
            Polygon([(77.54,12.89),(77.63,12.89),(77.63,12.94),(77.54,12.94)]),
        ],
        crs="EPSG:4326",
    )

    places.to_file(out / "places.geojson", driver="GeoJSON")
    zones.to_file(out / "zones.geojson", driver="GeoJSON")
    print("Created places.geojson and zones.geojson")


if __name__ == "__main__":
    create()
