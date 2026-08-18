# Technical Report – Automated Spatial Analysis Engine

## 1. Problem definition

Manual GIS analysis becomes slow and error-prone when the same sequence of tools must be repeated for many datasets. This project implements an automated spatial analysis engine that exposes common analysis operations as reusable Python functions and a single end-to-end workflow.

## 2. Architecture

The engine follows a modular architecture. Individual modules implement a single analytical concern while `SpatialAnalysisEngine` acts as a facade for end-to-end workflows. The CLI provides a reproducible entry point for execution from the shell.

## 3. Implemented analyses

### Buffer generation

Facility points are buffered by a configurable distance in a projected CRS.

### Overlay analysis

Facility buffers are intersected with parcel polygons to identify affected areas.

### Spatial join

Facility points are assigned to zones using a point-within-polygon spatial predicate.

### Network proximity

Facility-to-road distance is calculated against a road network. A graph utility is also supplied for shortest path estimation between snapped network nodes.

### Suitability modelling

Three criteria are normalised to 0–1 and combined using a weighted linear combination. Cost criteria are inverted so higher scores always represent greater suitability.

### Terrain derivatives

Slope and aspect are calculated from a DEM using spatial gradients and written as GeoTIFF rasters.

### Batch processing

The batch module applies a user-supplied processor to every input matching a pattern, allowing the same operation to run across many files.

### Report generation

The engine writes Markdown and JSON reports containing workflow results and a qualitative comparison between manual and automated GIS processing.

## 4. Manual versus automated workflow

A manual workflow requires repeatedly opening layers, selecting tools, supplying parameters, managing intermediate outputs, and recording results. The automated workflow stores these choices in executable code, executes them in a fixed order, and records the outcome in logs and reports. This reduces repetitive interaction and improves reproducibility.

## 5. Limitations

The network proximity demonstration uses a supplied road layer rather than downloading a live network from OpenStreetMap. This keeps the demonstration deterministic and offline-capable. The terrain computation assumes a projected or reasonably regular raster grid. For large production datasets, spatial indexes, chunked raster processing and parallel batch execution should be considered.
