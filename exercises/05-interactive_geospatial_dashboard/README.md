# Interactive Geospatial Dashboard

Exercise 05 for **GEOIN C12-P – Script Programming**.

## Technology choice

This exercise uses **Streamlit** for the application interface, **Folium/streamlit-folium** for the interactive web map, and **Plotly** for charts.

## Features

- Interactive web map
- Layer controls
- Search functionality
- Pop-up information
- Interactive charts
- Statistical summaries
- Filtering
- CSV and GeoJSON export
- Automated test

## Quick start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
streamlit run app/main.py
```

Then open the local Streamlit URL shown in the terminal.

## Test

```powershell
pytest
```
