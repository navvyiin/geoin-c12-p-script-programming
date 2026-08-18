"""High-level Earth observation workflow."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import rasterio
from .classification import build_training_labels, train_classifier, classify_image
from .change_detection import change_map, transition_matrix
from .indices import ndvi, ndwi
from .io import read_multispectral, write_raster
from .report import write_report, write_json
from .stats import area_statistics, raster_summary
from .visualisation import export_png, export_rgb_png

class RemoteSensingPipeline:
    def __init__(self, output_dir="outputs"):
        self.output_dir = Path(output_dir); self.output_dir.mkdir(parents=True, exist_ok=True)

    def _classify(self, bands):
        blue, green, red, nir = [bands[k].astype("float32") for k in ("blue", "green", "red", "nir")]
        labels = build_training_labels(blue, green, red, nir)
        model = train_classifier(blue, green, red, nir, labels)
        return classify_image(model, blue, green, red, nir)

    def process_scene(self, raster_path):
        profile, bands = read_multispectral(raster_path)
        blue, green, red, nir = [bands[k].astype("float32") for k in ("blue", "green", "red", "nir")]
        out_profile = profile.copy(); out_profile["count"] = 1
        ndvi_arr, ndwi_arr = ndvi(red, nir), ndwi(green, nir)
        write_raster(self.output_dir/"ndvi.tif", ndvi_arr, out_profile)
        write_raster(self.output_dir/"ndwi.tif", ndwi_arr, out_profile)
        classified = self._classify(bands)
        write_raster(self.output_dir/"land_cover_classification.tif", classified, out_profile, dtype="uint8", nodata=0)
        export_png(ndvi_arr, self.output_dir/"ndvi_map.png", "NDVI", "RdYlGn")
        export_png(ndwi_arr, self.output_dir/"ndwi_map.png", "NDWI", "Blues")
        export_png(classified, self.output_dir/"land_cover_map.png", "Introductory Land-Cover Classification", "tab10")
        export_rgb_png(blue, green, red, self.output_dir/"false_colour_composite.png")
        return {"source_raster": str(raster_path), "shape": list(red.shape), "crs": str(profile.get("crs")), "ndvi_stats": raster_summary(ndvi_arr), "ndwi_stats": raster_summary(ndwi_arr), "class_area_statistics": area_statistics(classified, profile)}

    def run_change_detection(self, before_path, after_path):
        _, before_bands = read_multispectral(before_path); _, after_bands = read_multispectral(after_path)
        before, after = self._classify(before_bands), self._classify(after_bands)
        changed = change_map(before, after)
        with rasterio.open(before_path) as src:
            profile = src.profile.copy(); profile["count"] = 1; pixel_area = abs(src.transform.a * src.transform.e)
        write_raster(self.output_dir/"land_cover_change.tif", changed, profile, dtype="uint8", nodata=0)
        export_png(changed, self.output_dir/"land_cover_change_map.png", "Land-Cover Change", "Reds")
        cp = int(np.count_nonzero(changed))
        return {"changed_pixels": cp, "changed_area_ha": cp * pixel_area / 10000.0, "transition_matrix": transition_matrix(before, after)}

    def run_full_workflow(self, scene_path, before_path=None, after_path=None):
        result = self.process_scene(scene_path)
        if before_path and after_path:
            result["change_detection"] = self.run_change_detection(before_path, after_path)
        write_report(self.output_dir/"scientific_report.md", result); write_json(self.output_dir/"summary_statistics.json", result)
        return result
