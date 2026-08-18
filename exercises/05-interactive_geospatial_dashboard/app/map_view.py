from __future__ import annotations

import folium
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium


def build_map(places, zones, selected_name: str | None = None):
    center = [12.97, 77.59]
    if not places.empty:
        center = [float(places.geometry.y.mean()), float(places.geometry.x.mean())]

    m = folium.Map(location=center, zoom_start=12, control_scale=True)

    folium.GeoJson(
        zones.to_json(),
        name="Zones",
        style_function=lambda _: {
            "fillColor": "#4C78A8",
            "color": "#1F4E79",
            "weight": 2,
            "fillOpacity": 0.18,
        },
        tooltip=GeoJsonTooltip(
            fields=["zone_name", "priority", "score"],
            aliases=["Zone", "Priority", "Score"],
            localize=True,
        ),
        show=True,
    ).add_to(m)

    for _, row in places.iterrows():
        highlighted = selected_name == row["name"]
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=9 if highlighted else 6,
            color="#D62728" if highlighted else "#2C7FB8",
            fill=True,
            fill_opacity=0.85,
            popup=folium.Popup(
                f"""
                <b>{row['name']}</b><br>
                Category: {row['category']}<br>
                Population: {row['population']:,}<br>
                Value: {row['value']}
                """,
                max_width=280,
            ),
            tooltip=row["name"],
        ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    return m


def render_map(m):
    return st_folium(m, width=None, height=560, returned_objects=[])
