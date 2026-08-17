# Technical Documentation

## 1. Scope

The toolkit is intended for introductory-to-intermediate geospatial data processing. Vector workflows use GeoPandas/Shapely/Fiona, coordinate reference systems use PyProj, and raster workflows use Rasterio.

## 2. Processing model

Each operation follows a simple pattern:

1. Load the source dataset.
2. Inspect and validate its CRS.
3. Perform one isolated geospatial operation.
4. Export the result explicitly.
5. Record the operation in a processing log.

This makes workflows reproducible and easier to debug.

## 3. Vector support

Supported formats include ESRI Shapefile, GeoPackage, GeoJSON, FlatGeobuf and GeoParquet. The toolkit uses a `GeoDataFrame` as the in-memory representation.

### CRS validation

`validate_crs()` checks whether a CRS is assigned. If an expected CRS is provided, it also reports whether the actual CRS matches it.

### Reprojection

`reproject_vector()` uses GeoPandas `to_crs()`. The input must already have a valid CRS because reprojection without a source CRS is ambiguous.

### Clipping

`clip_vector()` aligns the mask CRS with the input CRS and then performs a spatial clip.

### Merging

`merge_vectors()` aligns all input layers to the CRS of the first dataset and concatenates them into one GeoDataFrame.

## 4. Raster support

Raster operations are implemented through Rasterio. The toolkit supports raster CRS reprojection, raster clipping and mosaicking.

`reproject_raster()` calculates a target transform and output dimensions, then reprojects each raster band.

`clip_raster()` transforms the clipping geometry to the raster CRS when necessary and uses Rasterio's masking operation.

`merge_rasters()` creates a mosaic from multiple raster inputs with a shared coordinate system.

## 5. Metadata

Vector metadata includes feature count, fields, CRS, bounds and geometry-type frequencies. Raster metadata includes dimensions, band count, data type, CRS, transform, bounds and NoData value.

## 6. Logging

Every high-level operation made through `GeoProcessor` is retained in memory and can be written to JSON with `save_log()`. A normal text log is also written by Python's logging module.

The JSON log is useful for report generation and reproducibility because it records the operation name, inputs and important result properties.

## 7. Error handling

The package fails early for common invalid states, including:

- Missing CRS when reprojection is requested
- Missing CRS on clipping masks
- Unsupported file extensions
- Empty merge requests
- Unknown vector output formats

## 8. Extending the toolkit

New operations should be added to `operations.py`, exposed through `GeoProcessor` when they represent a high-level workflow, and tested in `tests/`. A command-line subcommand can then be added in `cli.py`.
