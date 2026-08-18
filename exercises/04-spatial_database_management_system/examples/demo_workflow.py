from pathlib import Path
import json

from spatial_db.core import SpatialDatabaseApp


def main():
    root = Path(__file__).resolve().parents[1]
    db_path = root / "outputs" / "spatial_database.gpkg"
    sample_dir = root / "sample_data"
    output_dir = root / "outputs"
    output_dir.mkdir(exist_ok=True)

    if not (sample_dir / "places.geojson").exists():
        import subprocess, sys
        subprocess.run([sys.executable, str(root / "examples" / "create_sample_data.py")], check=True)

    if db_path.exists():
        db_path.unlink()

    app = SpatialDatabaseApp(db_path)
    imported_places = app.import_dataset(sample_dir / "places.geojson", "places")
    imported_zones = app.import_dataset(sample_dir / "zones.geojson", "zones")

    high_population = app.query_attribute("places", "population", ">=", 8000)
    high_population_path = app.export(
        high_population, output_dir / "high_population_places.geojson"
    )

    in_zones = app.query_intersection("places", "zones")
    intersection_path = app.export(
        in_zones, output_dir / "places_intersecting_zones.geojson"
    )

    updated = app.update_records(
        "places", "category", "Priority Urban", "place_id", 1
    )

    nearest = app.query_nearest("places", "zones")
    nearest_path = app.export(
        nearest, output_dir / "places_nearest_distance.geojson"
    )

    summary = app.summary(output_dir)

    result = {
        "database": str(db_path),
        "imported_places": imported_places,
        "imported_zones": imported_zones,
        "attribute_query_matches": len(high_population),
        "attribute_query_output": str(high_population_path),
        "spatial_query_matches": len(in_zones),
        "spatial_query_output": str(intersection_path),
        "records_updated": updated,
        "nearest_output": str(nearest_path),
        "layer_count": len(summary["layers"]),
        "status": "completed",
    }

    (output_dir / "demo_summary.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print("Demonstration complete.")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
