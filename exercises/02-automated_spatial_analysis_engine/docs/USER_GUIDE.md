# User Guide

## Installation

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Run the complete workflow

```powershell
python examples\demo_workflow.py
```

## Run through the CLI

```powershell
spatial-engine demo
```

Optional parameters:

```powershell
spatial-engine demo --sample-dir sample_data --output-dir outputs --log logs/process.log
```

## Outputs

The demonstration produces GeoPackage vector layers, GeoTIFF terrain derivatives and Markdown/JSON reports in `outputs/`.
