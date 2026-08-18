"""Run the complete Earth observation demonstration."""
from pathlib import Path
import json, subprocess, sys, time
ROOT=Path(__file__).resolve().parents[1]; sample=ROOT/"sample_data"; out=ROOT/"outputs"; out.mkdir(exist_ok=True)
if not (sample/"scene_2023.tif").exists(): subprocess.run([sys.executable,str(ROOT/"examples"/"create_sample_data.py")],check=True)
from rs_pipeline.core import RemoteSensingPipeline
start=time.perf_counter(); result=RemoteSensingPipeline(out).run_full_workflow(sample/"scene_2024.tif",sample/"scene_2023.tif",sample/"scene_2024.tif"); elapsed=time.perf_counter()-start
result["workflow_seconds"]=elapsed; (out/"summary_statistics.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print("Demonstration complete."); print(f"NDVI mean: {result['ndvi_stats']['mean']:.4f}"); print(f"NDWI mean: {result['ndwi_stats']['mean']:.4f}"); print(f"Changed pixels: {result['change_detection']['changed_pixels']}"); print(f"Changed area (ha): {result['change_detection']['changed_area_ha']:.4f}"); print(f"Workflow seconds: {elapsed:.4f}"); print("Status: completed")
