# User Guide

## Installation

Use a Python 3.10+ environment and install the package with `pip install -e .`.

## Recommended workflow

Always inspect the CRS before combining layers. Keep intermediate outputs when a workflow is complex, and write the final processing log after the operation sequence completes.

## Common tasks

### Read and inspect

```python
from geotoolkit import GeoProcessor
p = GeoProcessor()
gdf = p.read_vector("roads.gpkg")
print(p.metadata("roads.gpkg"))
```

### Reproject

```python
projected = p.reproject_vector(gdf, "EPSG:32643")
```

### Clip

```python
mask = p.read_vector("boundary.gpkg")
clipped = p.clip_vector(projected, mask)
```

### Export

```python
p.export_vector(clipped, "outputs/roads_clip.geojson")
```

### Log

```python
p.save_log("logs/processing.json")
```
