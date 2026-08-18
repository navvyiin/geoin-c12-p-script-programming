from __future__ import annotations

import argparse
from pathlib import Path

from .core import SpatialAnalysisEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Automated Spatial Analysis Engine")
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="run the complete demonstration workflow")
    demo.add_argument("--sample-dir", default="sample_data")
    demo.add_argument("--output-dir", default="outputs")
    demo.add_argument("--log", default="logs/process.log")
    args = parser.parse_args()
    if args.command == "demo":
        engine = SpatialAnalysisEngine(args.output_dir, args.log)
        result = engine.run_demo(args.sample_dir)
        print("Workflow completed")
        print(f"Output directory: {Path(args.output_dir).resolve()}")
        for k, v in result.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
