# Technical Documentation

## Objective

Exercise 04 implements a small spatial database management system for importing spatial datasets, executing attribute and spatial queries, updating records, producing summary reports, and exporting results.

## Local database

The default demonstration backend is a GeoPackage because it requires no server installation. GeoPackage is SQLite-based and supports vector layers with spatial metadata.

## PostgreSQL/PostGIS

The module `spatial_db.postgis` provides an introductory SQLAlchemy connector. A PostgreSQL/PostGIS URL can be supplied by a user with a running PostGIS server.

Example:

```text
postgresql+psycopg://username:password@localhost:5432/gisdb
```

The connection helper can test PostgreSQL and PostGIS availability.

## Query library

`spatial_db.queries` contains reusable attribute filtering, intersection, within and nearest-distance functions.

## Reproducibility

The sample data are deterministic and generated locally by `examples/create_sample_data.py`.
