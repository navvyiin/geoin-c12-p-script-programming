from __future__ import annotations

from pathlib import Path

from .db import import_layer, read_layer, list_layers, update_layer, export_layer
from .queries import attribute_filter, spatial_intersection, spatial_within, nearest_distance
from .reports import summarise_layer, write_summary_report, write_json_report


class SpatialDatabaseApp:
    """High-level geospatial database management application."""

    def __init__(self, db_path: str | Path = "outputs/spatial_database.gpkg"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def import_dataset(self, source_path, layer_name) -> int:
        return import_layer(self.db_path, source_path, layer_name)

    def layers(self) -> list[str]:
        return list_layers(self.db_path)

    def query_attribute(self, layer_name, column, operator, value):
        gdf = read_layer(self.db_path, layer_name)
        return attribute_filter(gdf, column, operator, value)

    def query_intersection(self, layer_name, mask_layer):
        features = read_layer(self.db_path, layer_name)
        mask = read_layer(self.db_path, mask_layer)
        return spatial_intersection(features, mask)

    def query_within(self, layer_name, mask_layer):
        features = read_layer(self.db_path, layer_name)
        mask = read_layer(self.db_path, mask_layer)
        return spatial_within(features, mask)

    def query_nearest(self, layer_name, target_layer):
        features = read_layer(self.db_path, layer_name)
        targets = read_layer(self.db_path, target_layer)
        return nearest_distance(features, targets)

    def update_records(self, layer_name, column, value, where_column, where_value) -> int:
        gdf = read_layer(self.db_path, layer_name)
        if where_column not in gdf.columns or column not in gdf.columns:
            raise KeyError("Specified update fields do not exist.")
        mask = gdf[where_column] == where_value
        count = int(mask.sum())
        gdf.loc[mask, column] = value
        update_layer(self.db_path, layer_name, gdf)
        return count

    def export(self, gdf, output_path, layer="query_result"):
        return export_layer(gdf, output_path, layer=layer)

    def summary(self, output_dir="outputs") -> dict:
        summaries = [summarise_layer(read_layer(self.db_path, layer), layer) for layer in self.layers()]
        payload = {"database": str(self.db_path), "layers": summaries}
        output_dir = Path(output_dir)
        write_summary_report(output_dir / "summary_report.md", summaries)
        write_json_report(output_dir / "summary_report.json", payload)
        return payload
