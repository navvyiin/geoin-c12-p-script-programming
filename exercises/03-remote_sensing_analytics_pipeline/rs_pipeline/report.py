"""Scientific report generation."""
from __future__ import annotations
from pathlib import Path
import json

def write_report(path, payload):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Remote Sensing Analytics Pipeline Report", "", "## Workflow", f"- Source raster: `{payload.get('source_raster', '')}`", f"- Image dimensions: {payload.get('shape', '')}", f"- CRS: `{payload.get('crs', '')}`", "", "## NDVI statistics"]
    for k, v in payload.get("ndvi_stats", {}).items(): lines.append(f"- **{k}:** {v}")
    lines += ["", "## NDWI statistics"]
    for k, v in payload.get("ndwi_stats", {}).items(): lines.append(f"- **{k}:** {v}")
    lines += ["", "## Land-cover area statistics", "", "| Class | Pixels | Area (ha) | Percentage |", "|---|---:|---:|---:|"]
    for row in payload.get("class_area_statistics", []): lines.append(f"| {row['class_id']} | {row['pixel_count']} | {row['area_ha']:.4f} | {row['percentage']:.2f}% |")
    cd = payload.get("change_detection", {})
    lines += ["", "## Change detection", f"- Changed pixels: {cd.get('changed_pixels', 0)}", f"- Changed area (ha): {cd.get('changed_area_ha', 0.0):.4f}", ""]
    path.write_text("\n".join(lines), encoding="utf-8")

def write_json(path, payload):
    Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
