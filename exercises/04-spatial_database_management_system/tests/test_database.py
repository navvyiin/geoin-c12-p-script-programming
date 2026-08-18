from pathlib import Path

from spatial_db.core import SpatialDatabaseApp


def test_end_to_end(tmp_path: Path):
    from examples.create_sample_data import create
    import shutil

    root = Path(__file__).resolve().parents[1]
    sample = root / "sample_data"
    create()

    db = tmp_path / "test.gpkg"
    app = SpatialDatabaseApp(db)
    assert app.import_dataset(sample / "places.geojson", "places") == 5
    assert app.import_dataset(sample / "zones.geojson", "zones") == 3

    assert len(app.layers()) == 2
    result = app.query_attribute("places", "population", ">=", 8000)
    assert len(result) == 3

    spatial = app.query_intersection("places", "zones")
    assert len(spatial) == 4

    updated = app.update_records("places", "category", "Updated", "place_id", 1)
    assert updated == 1

    summary = app.summary(tmp_path)
    assert len(summary["layers"]) == 2
