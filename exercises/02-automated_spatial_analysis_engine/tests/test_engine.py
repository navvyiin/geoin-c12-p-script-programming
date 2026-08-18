from pathlib import Path

import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

from spatial_engine.buffer_analysis import generate_buffers
from spatial_engine.suitability import SuitabilityCriterion, weighted_suitability

def test_buffer_generation():
    gdf = gpd.GeoDataFrame({"id":[1,2], "geometry":[Point(0,0), Point(1,1)]}, crs="EPSG:3857")
    out = generate_buffers(gdf, 10)
    assert len(out) == 2
    assert out.geometry.iloc[0].area > 300

def test_suitability_ranking():
    df = pd.DataFrame({"cost":[1,2,3], "benefit":[3,2,1]})
    out = weighted_suitability(df, [SuitabilityCriterion("cost",0.5,"cost"), SuitabilityCriterion("benefit",0.5,"benefit")])
    assert "suitability_score" in out.columns
    assert out.iloc[0]["suitability_score"] >= out.iloc[-1]["suitability_score"]

def test_demo_exists_after_generation(tmp_path):
    assert Path("examples/demo_workflow.py").exists()
