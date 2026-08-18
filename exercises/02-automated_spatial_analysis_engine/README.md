# Automated Spatial Analysis Engine

Exercise 02 for **GEOIN C12-P – Script Programming**.

This project implements a reusable Python application for automating common GIS analyses and turning them into a repeatable workflow. It covers buffer generation, overlay analysis, spatial joins, network proximity, suitability modelling, terrain derivatives, batch processing, reporting, and performance evaluation.

## Objectives

- Replace repetitive manual GIS operations with scripted workflows.
- Keep analysis parameters explicit and reproducible.
- Process multiple datasets consistently in batch mode.
- Produce machine-readable and human-readable reports.
- Compare automated processing with a documented manual workflow.

## Main capabilities

| Capability | Module |
|---|---|
| Buffer generation | `buffer_analysis.py` |
| Overlay analysis | `overlay_analysis.py` |
| Spatial joins | `spatial_join_analysis.py` |
| Network proximity | `network_analysis.py` |
| Suitability modelling | `suitability.py` |
| Terrain derivatives | `terrain.py` |
| Batch processing | `batch.py` |
| Reporting | `report.py` |
| CLI | `cli.py` |

## Quick start

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python examples\demo_workflow.py
pytest
spatial-engine --help
```

The demonstration creates synthetic sample data, executes the complete workflow, writes outputs into `outputs/`, and produces a Markdown report plus machine-readable JSON.

## Project structure

```text
spatial_engine/
  __init__.py
  cli.py
  core.py
  buffer_analysis.py
  overlay_analysis.py
  spatial_join_analysis.py
  network_analysis.py
  suitability.py
  terrain.py
  batch.py
  report.py
  utils.py
sample_data/
examples/
tests/
docs/
outputs/
logs/
```

## Reproducibility

The demonstration uses synthetic data so it can be executed without internet access or proprietary datasets. Replace the sample layers with real GeoPackage, GeoJSON, Shapefile, or raster inputs when adapting the engine to real studies.

## Academic deliverables

- Executable Python programme
- Automated end-to-end workflow
- Technical report
- Performance evaluation
- Unit tests
- Sample datasets
- Documentation
