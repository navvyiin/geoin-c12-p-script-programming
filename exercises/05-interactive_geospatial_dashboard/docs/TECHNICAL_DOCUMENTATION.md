# Technical Documentation

## Architecture

The application is divided into:

- `app/data.py`: sample data generation and layer loading
- `app/analytics.py`: filtering, summaries and export helpers
- `app/map_view.py`: Folium map construction and Streamlit embedding
- `app/main.py`: Streamlit user interface

## Mapping

Folium is used for web-map rendering. Streamlit-Folium embeds the Folium map inside Streamlit and supports interactive map controls and pop-ups.

## Charts

Plotly Express provides the statistical charts.

## Data flow

```text
GeoJSON layers
      ↓
Load into GeoDataFrames
      ↓
Sidebar search / filtering
      ↓
Filtered data
      ├── Map
      ├── Statistics
      ├── Charts
      └── Exports
```

## Extending the application

Replace the sample GeoJSON data under `sample_data/` with real vector layers, keeping compatible attribute names or updating `app/analytics.py` and `app/main.py`.
