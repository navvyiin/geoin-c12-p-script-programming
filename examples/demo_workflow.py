from __future__ import annotations

import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.transform import from_origin
from shapely.geometry import Point, Polygon

from geotoolkit import GeoProcessor
from geotoolkit.io import write_vector

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "sample_data"
OUTPUT = ROOT / "outputs"
LOGS = ROOT / "logs"


def create_sample_data() -> None:
    SAMPLE.mkdir(exist_ok=True)
    # Point dataset in WGS84.
    cities = gpd.GeoDataFrame(
        {
            "name": ["Alpha", "Beta", "Gamma", "Delta"],
            "population": [12000, 19500, 8000, 14000],
        },
        geometry=[Point(77.55, 12.96), Point(77.59, 12.98), Point(77.63, 13.01), Point(77.49, 12.93)],
        crs="EPSG:4326",
    )
    cities.to_file(SAMPLE / "cities.geojson", driver="GeoJSON")

    extra = gpd.GeoDataFrame(
        {"name": ["Epsilon", "Zeta"], "population": [6000, 9500]},
        geometry=[Point(77.61, 12.95), Point(77.52, 12.99)],
        crs="EPSG:4326",
    )
    extra.to_file(SAMPLE / "points_extra.geojson", driver="GeoJSON")

    study_area = gpd.GeoDataFrame(
        {"zone": ["Study Area"]},
        geometry=[Polygon([(77.48, 12.92), (77.66, 12.92), (77.66, 13.03), (77.48, 13.03)])],
        crs="EPSG:4326",
    )
    study_area.to_file(SAMPLE / "study_area.geojson", driver="GeoJSON")

    # 60 x 60 synthetic raster in WGS84.
    raster_path = SAMPLE / "surface.tif"
    width = height = 60
    transform = from_origin(77.45, 13.08, 0.003, 0.003)
    yy, xx = np.mgrid[0:height, 0:width]
    data = ((xx + yy) / (width + height) * 100).astype("float32")
    profile = {
        "driver": "GTiff",
        "height": height,
        "width": width,
        "count": 1,
        "dtype": "float32",
        "crs": "EPSG:4326",
        "transform": transform,
        "nodata": -9999.0,
    }
    with rasterio.open(raster_path, "w", **profile) as dst:
        dst.write(data, 1)


def main() -> None:
    create_sample_data()
    OUTPUT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)

    p = GeoProcessor(log_path=LOGS / "demo_processing.log")
    cities = p.read_vector(SAMPLE / "cities.geojson")
    extra = p.read_vector(SAMPLE / "points_extra.geojson")
    mask = p.read_vector(SAMPLE / "study_area.geojson")

    p.validate_crs(cities, "EPSG:4326")
    cities_3857 = p.reproject_vector(cities, "EPSG:3857")
    mask_3857 = p.reproject_vector(mask, "EPSG:3857")
    clipped = p.clip_vector(cities_3857, mask_3857)
    merged = p.merge_vectors([cities, extra])

    p.export_vector(clipped, OUTPUT / "cities_clipped.gpkg", layer="cities")
    p.export_vector(merged, OUTPUT / "merged_points.geojson")
    try:
        p.export_vector(merged, OUTPUT / "merged_points.parquet")
        parquet_status = "created"
    except ImportError:
        parquet_status = "skipped: install pyarrow to enable GeoParquet export"

    raster_clipped = p.clip_raster(SAMPLE / "surface.tif", mask, OUTPUT / "surface_clipped.tif")
    raster_projected = p.reproject_raster(raster_clipped, OUTPUT / "surface_3857.tif", "EPSG:3857")

    metadata = {
        "cities": p.metadata(SAMPLE / "cities.geojson"),
        "study_area": p.metadata(SAMPLE / "study_area.geojson"),
        "surface": p.metadata(SAMPLE / "surface.tif"),
        "parquet": parquet_status,
        "outputs": [str(path.relative_to(ROOT)) for path in OUTPUT.iterdir()],
    }
    (OUTPUT / "demo_metadata.json").write_text(json.dumps(metadata, indent=2, default=str), encoding="utf-8")
    p.save_log(LOGS / "demo_processing.json")

    print("Demonstration complete.")
    print(f"Outputs: {OUTPUT}")
    print(f"Logs: {LOGS}")
    print(f"GeoParquet: {parquet_status}")


if __name__ == "__main__":
    main()
