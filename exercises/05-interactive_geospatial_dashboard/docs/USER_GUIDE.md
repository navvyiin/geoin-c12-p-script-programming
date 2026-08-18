# User Guide

## Install

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Run the dashboard

```powershell
streamlit run app/main.py
```

Streamlit will provide a local URL, normally `http://localhost:8501`.

## Features

- Interactive Folium map
- Layer controls
- Search by place name
- Category and numeric filters
- Marker pop-ups and tooltips
- Plotly charts
- Summary statistics
- CSV export
- GeoJSON export

## Testing

```powershell
pytest
```
