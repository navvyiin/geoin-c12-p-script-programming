"""Raster statistics and area calculations."""
from __future__ import annotations
import json
import numpy as np

def area_statistics(class_map, profile, pixel_area_m2=None):
    if pixel_area_m2 is None:
        transform = profile["transform"]
        pixel_area_m2 = abs(transform.a * transform.e)
    total = int(np.count_nonzero(class_map))
    rows = []
    for cls in sorted(int(v) for v in np.unique(class_map) if v != 0):
        count = int(np.count_nonzero(class_map == cls))
        area_m2 = count * pixel_area_m2
        rows.append({"class_id": cls, "pixel_count": count, "area_m2": float(area_m2), "area_ha": float(area_m2 / 10000.0), "percentage": float(count / total * 100.0 if total else 0.0)})
    return rows

def raster_summary(array):
    valid = array[np.isfinite(array)]
    if valid.size == 0:
        return {"count": 0}
    return {"count": int(valid.size), "min": float(valid.min()), "max": float(valid.max()), "mean": float(valid.mean()), "median": float(np.median(valid)), "std": float(valid.std())}

def save_json(path, payload):
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
