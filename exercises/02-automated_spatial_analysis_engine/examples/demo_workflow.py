from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "sample_data"

# Make the example independently runnable.
if not (DATA / "facilities.geojson").exists():
    subprocess.run([sys.executable, str(ROOT / "examples" / "create_sample_data.py")], check=True)

from spatial_engine import SpatialAnalysisEngine

engine = SpatialAnalysisEngine(ROOT / "outputs", ROOT / "logs" / "process.log")
results = engine.run_demo(DATA)
print("\nDemonstration complete.")
for k, v in results.items():
    print(f"{k}: {v}")
