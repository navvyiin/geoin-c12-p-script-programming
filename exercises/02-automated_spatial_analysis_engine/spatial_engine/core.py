from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import geopandas as gpd

from .batch import batch_process
from .buffer_analysis import generate_buffers
from .network_analysis import nearest_network_distance, shortest_path_distance
from .overlay_analysis import intersection
from .report import build_report
from .spatial_join_analysis import spatial_join
from .suitability import SuitabilityCriterion, weighted_suitability
from .terrain import slope_aspect
from .utils import ensure_dir, setup_logger, write_vector


class SpatialAnalysisEngine:
    """High-level facade for reproducible spatial analysis workflows."""

    def __init__(self, output_dir: str | Path = "outputs", log_path: str | Path = "logs/process.log") -> None:
        self.output_dir = ensure_dir(output_dir)
        ensure_dir(Path(log_path).parent)
        self.logger = setup_logger(log_path)
        self.results: dict[str, Any] = {}

    def run_demo(self, sample_dir: str | Path = "sample_data") -> dict[str, Any]:
        sample_dir = Path(sample_dir)
        t0 = time.perf_counter()
        facilities = gpd.read_file(sample_dir / "facilities.geojson")
        zones = gpd.read_file(sample_dir / "zones.geojson")
        roads = gpd.read_file(sample_dir / "roads.geojson")
        parcels = gpd.read_file(sample_dir / "parcels.geojson")

        projected = facilities.to_crs("EPSG:32643")
        zones_p = zones.to_crs(projected.crs)
        roads_p = roads.to_crs(projected.crs)
        parcels_p = parcels.to_crs(projected.crs)

        buffers = generate_buffers(projected, 250)
        write_vector(buffers, self.output_dir / "facility_buffers.gpkg")
        self.results["buffer_features"] = len(buffers)

        overlay = intersection(parcels_p, buffers[["geometry"]])
        write_vector(overlay, self.output_dir / "parcel_buffer_intersection.gpkg")
        self.results["overlay_features"] = len(overlay)

        joined = spatial_join(facilities.to_crs(zones.crs), zones, predicate="within")
        write_vector(joined, self.output_dir / "facility_zone_join.gpkg")
        self.results["spatial_join_matches"] = int(joined["index_right"].notna().sum())

        network = nearest_network_distance(projected, roads_p)
        write_vector(network, self.output_dir / "facility_network_proximity.gpkg")
        self.results["mean_network_distance"] = float(network["network_distance"].mean())
        self.results["sample_shortest_path_distance"] = shortest_path_distance(projected.geometry.iloc[0], projected.geometry.iloc[3], roads_p)

        suitability_input = parcels_p[["parcel_id", "land_value", "road_distance", "elevation", "geometry"]].copy()
        criteria = [
            SuitabilityCriterion("land_value", 0.40, "cost"),
            SuitabilityCriterion("road_distance", 0.30, "cost"),
            SuitabilityCriterion("elevation", 0.30, "benefit"),
        ]
        suitable = weighted_suitability(suitability_input, criteria)
        write_vector(suitable, self.output_dir / "suitability.gpkg")
        self.results["top_suitability_score"] = float(suitable["suitability_score"].iloc[0])

        batch_input = sample_dir / "batch_inputs"
        batch_output = self.output_dir / "batch_outputs"
        def _batch_reproject(src, dst):
            layer = gpd.read_file(src).to_crs("EPSG:32643")
            write_vector(layer, Path(dst).with_suffix(".gpkg"))
        batch_files = batch_process(batch_input, batch_output, _batch_reproject, pattern="*.geojson")
        self.results["batch_files_processed"] = len(batch_files)

        dem = sample_dir / "dem.tif"
        terrain_paths = slope_aspect(dem, self.output_dir / "slope.tif", self.output_dir / "aspect.tif")
        self.results["terrain_derivatives"] = terrain_paths

        elapsed = time.perf_counter() - t0
        self.results["workflow_seconds"] = elapsed
        self.results["status"] = "completed"
        self.logger.info("workflow=%s", self.results)
        build_report(self.results, self.output_dir / "technical_report.md", self.output_dir / "technical_report.json")
        return self.results
