from pathlib import Path
import time
from statistics import mean, stdev

from spatial_engine import SpatialAnalysisEngine

ROOT = Path(__file__).resolve().parents[1]
times = []
for _ in range(3):
    out = ROOT / "outputs" / "benchmark"
    engine = SpatialAnalysisEngine(out, ROOT / "logs" / "benchmark.log")
    t0 = time.perf_counter()
    engine.run_demo(ROOT / "sample_data")
    times.append(time.perf_counter() - t0)

print(f"runs={len(times)}")
print(f"mean_seconds={mean(times):.6f}")
print(f"stdev_seconds={stdev(times):.6f}")
print("raw_seconds=" + ",".join(f"{x:.6f}" for x in times))
