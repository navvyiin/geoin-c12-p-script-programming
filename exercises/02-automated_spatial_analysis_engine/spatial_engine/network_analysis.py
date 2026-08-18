from __future__ import annotations

from math import hypot
from typing import Iterable

import geopandas as gpd
import networkx as nx
from shapely.geometry import Point


def graph_from_lines(lines: gpd.GeoDataFrame) -> nx.Graph:
    """Build a weighted undirected graph from LineString geometries."""
    graph = nx.Graph()
    for geom in lines.geometry:
        coords = list(geom.coords)
        for a, b in zip(coords, coords[1:]):
            w = hypot(b[0] - a[0], b[1] - a[1])
            graph.add_edge(tuple(a), tuple(b), weight=w)
    return graph


def nearest_network_distance(points: gpd.GeoDataFrame, lines: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Return distance from each point to the nearest network edge."""
    if points.crs != lines.crs:
        lines = lines.to_crs(points.crs)
    union = lines.geometry.union_all()
    out = points.copy()
    out["network_distance"] = out.geometry.distance(union)
    return out

def shortest_path_distance(start: Point, end: Point, lines: gpd.GeoDataFrame) -> float:
    """Approximate shortest graph distance between two points by snapping to nearest nodes."""
    graph = graph_from_lines(lines)
    nodes = list(graph.nodes)
    s = min(nodes, key=lambda n: start.distance(Point(n)))
    e = min(nodes, key=lambda n: end.distance(Point(n)))
    return float(nx.shortest_path_length(graph, s, e, weight="weight"))
