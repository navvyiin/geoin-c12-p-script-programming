from __future__ import annotations

from pathlib import Path
import streamlit as st
import plotly.express as px

from app.analytics import filter_places, summary_stats, category_summary, to_csv_bytes, to_geojson_bytes
from app.data import load_layers
from app.map_view import build_map, render_map


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "sample_data"


st.set_page_config(
    page_title="Interactive Geospatial Dashboard",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🗺️ Interactive Geospatial Dashboard")
st.caption("Exercise 05 · GEOIN C12-P – Script Programming")

places, zones = load_layers(DATA_DIR)

with st.sidebar:
    st.header("Layer Controls")
    show_places = st.checkbox("Show place markers", value=True)
    show_zones = st.checkbox("Show zones", value=True)

    st.header("Search")
    search = st.text_input("Search place name", placeholder="e.g. Central")

    st.header("Filters")
    categories = sorted(places["category"].unique().tolist())
    selected_categories = st.multiselect("Categories", categories, default=categories)
    min_population, max_population = st.slider(
        "Population range",
        int(places["population"].min()),
        int(places["population"].max()),
        (int(places["population"].min()), int(places["population"].max())),
        step=100,
    )
    min_value = st.slider("Minimum value", 0, 100, 0)

filtered = filter_places(
    places,
    categories=selected_categories,
    min_population=min_population,
    max_population=max_population,
    min_value=min_value,
)

if search.strip():
    filtered = filtered[filtered["name"].str.contains(search.strip(), case=False, na=False)]

# Respect visibility controls.
map_places = filtered if show_places else filtered.iloc[0:0]
map_zones = zones if show_zones else zones.iloc[0:0]

stats = summary_stats(filtered)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Features", stats["feature_count"])
c2.metric("Population", f"{stats['total_population']:,}")
c3.metric("Mean Value", f"{stats['mean_value']:.1f}")
c4.metric("Top Category", stats["top_category"])

st.subheader("Interactive Map")
selected_name = filtered.iloc[0]["name"] if search.strip() and len(filtered) == 1 else None
m = build_map(map_places, map_zones, selected_name=selected_name)
render_map(m)

left, right = st.columns(2)

with left:
    st.subheader("Category Summary")
    cat = category_summary(filtered)
    if not cat.empty:
        fig = px.bar(
            cat,
            x="category",
            y="population",
            text="population",
            title="Population by Category",
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No records match the current filters.")

with right:
    st.subheader("Value Distribution")
    if not filtered.empty:
        fig = px.histogram(
            filtered,
            x="value",
            nbins=10,
            title="Value Distribution",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No records match the current filters.")

st.subheader("Filtered Records")
display_columns = ["id", "name", "population", "category", "value"]
st.dataframe(filtered[display_columns], use_container_width=True, hide_index=True)

st.subheader("Export")
e1, e2 = st.columns(2)
with e1:
    st.download_button(
        "Download CSV",
        data=to_csv_bytes(filtered),
        file_name="filtered_places.csv",
        mime="text/csv",
    )
with e2:
    st.download_button(
        "Download GeoJSON",
        data=to_geojson_bytes(filtered),
        file_name="filtered_places.geojson",
        mime="application/geo+json",
    )

st.info(
    "The supplied dataset is a small deterministic teaching dataset. "
    "The dashboard architecture is designed so the sample GeoJSON layers can be replaced with real GIS data."
)
