# Spatial Database Management System

Exercise 04 for GEOIN C12-P – Script Programming.

## Features

- Import spatial datasets
- Attribute queries
- Spatial intersection queries
- Nearest-distance analysis
- Record updates
- Summary report generation
- GeoPackage database management
- PostgreSQL/PostGIS introductory connector
- Database schema and reusable query library
- Query result export
- Automated tests

## Quick start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python examples\demo_workflow.py
pytest
spatial-db --help
```

The default workflow uses a local GeoPackage so it can be demonstrated without a PostgreSQL server.
