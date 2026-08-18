# Remote Sensing Analytics Pipeline

Exercise 03 for **GEOIN C12-P – Script Programming**.

## Objective
A Python-based Earth observation processing workflow for multispectral imagery.

## Implemented tasks
- Read multispectral imagery
- Compute NDVI
- Compute NDWI
- Introductory Random Forest image classification
- Calculate land-cover area statistics
- Detect basic land-cover changes
- Export thematic maps
- Generate summary statistics
- Generate a scientific report

## Quick start
```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -e ".[dev]"
python examples\\demo_workflow.py
pytest
spatial-engine-rs --help
```

## Note
The included scenes are synthetic Earth observation teaching data. Replace them with appropriately preprocessed real imagery for an applied study.
