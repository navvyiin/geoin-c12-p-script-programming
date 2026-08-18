from __future__ import annotations

from pathlib import Path
import json
import geopandas as gpd


def summarise_layer(gdf: gpd.GeoDataFrame, layer_name: str) -> dict:
    """Generate basic layer statistics."""
    geometry_types = {}
    if len(gdf):
        geometry_types = {
            str(k): int(v)
            for k, v in gdf.geometry.geom_type.value_counts().to_dict().items()
        }
    return {
        "layer": layer_name,
        "feature_count": int(len(gdf)),
        "columns": [c for c in gdf.columns if c != "geometry"],
        "crs": str(gdf.crs),
        "bounds": list(map(float, gdf.total_bounds)) if len(gdf) else None,
        "geometry_types": geometry_types,
    }


def write_summary_report(path: str | Path, summaries: list[dict]) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Spatial Database Summary Report",
        "",
        "## Layers",
        "",
        "| Layer | Features | CRS | Geometry types |",
        "|---|---:|---|---|",
    ]
    for s in summaries:
        lines.append(
            f"| {s['layer']} | {s['feature_count']} | {s['crs']} | {s['geometry_types']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_json_report(path: str | Path, payload: dict) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path
