# API Reference

## `GeoProcessor`

### `read_vector(path, layer=None)`
Returns a GeoDataFrame.

### `validate_crs(obj, expected=None)`
Returns a dictionary containing `has_crs`, `crs` and, when an expected CRS is supplied, `matches_expected`.

### `reproject_vector(gdf, target_crs)`
Returns a reprojected GeoDataFrame.

### `clip_vector(gdf, mask_gdf)`
Returns features clipped to the mask geometry.

### `merge_vectors(gdfs)`
Returns a single GeoDataFrame containing the supplied layers.

### `export_vector(gdf, path, layer=None)`
Exports the vector dataset using a driver inferred from the extension.

### `reproject_raster(src_path, dst_path, target_crs)`
Reprojects all raster bands and writes a new raster.

### `clip_raster(src_path, mask_gdf, dst_path)`
Clips a raster using polygon geometries.

### `merge_rasters(src_paths, dst_path)`
Creates a mosaic from raster sources.

### `metadata(path)`
Returns dataset metadata as a dictionary.

### `save_log(path)`
Writes the recorded high-level operations to JSON.
