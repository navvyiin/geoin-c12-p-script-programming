from pathlib import Path

from app.analytics import filter_places, summary_stats
from app.data import load_layers


def test_filter_and_summary(tmp_path: Path):
    places, zones = load_layers(tmp_path)
    result = filter_places(
        places,
        categories=["Urban"],
        min_population=8000,
        min_value=60,
    )
    assert len(result) == 2
    stats = summary_stats(result)
    assert stats["feature_count"] == 2
    assert stats["total_population"] == 20500
