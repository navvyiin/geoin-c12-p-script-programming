"""Command-line interface."""
from __future__ import annotations
import argparse
from pathlib import Path
from .core import RemoteSensingPipeline

def main():
    parser = argparse.ArgumentParser(description="Remote Sensing Analytics Pipeline")
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="run the complete demonstration workflow")
    demo.add_argument("--sample-dir", default="sample_data"); demo.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()
    sample = Path(args.sample_dir); pipe = RemoteSensingPipeline(args.output_dir)
    result = pipe.run_full_workflow(sample/"scene_2024.tif", sample/"scene_2023.tif", sample/"scene_2024.tif")
    print("Workflow completed"); print(f"NDVI mean: {result['ndvi_stats']['mean']:.4f}"); print(f"NDWI mean: {result['ndwi_stats']['mean']:.4f}"); print(f"Changed area (ha): {result['change_detection']['changed_area_ha']:.4f}"); print(f"Output directory: {Path(args.output_dir).resolve()}")

if __name__ == "__main__": main()
