# User Guide

## Installation

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Generate sample data

```powershell
python examples\create_sample_data.py
```

## Run the complete workflow

```powershell
python examples\demo_workflow.py
```

## Run tests

```powershell
pytest
```

## CLI

```powershell
spatial-db --help
spatial-db layers
spatial-db summary
```

## PostgreSQL/PostGIS

Install PostgreSQL with PostGIS separately, then use a SQLAlchemy connection URL with `spatial_db.postgis`.
