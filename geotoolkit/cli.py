from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import GeoProcessor
from .io import detect_type, read_vector, write_vector


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="geotool", description="Geospatial Data Processing Toolkit")
    sub = p.add_subparsers(dest="command", required=True)

    meta = sub.add_parser("metadata", help="Print dataset metadata as JSON")
    meta.add_argument("input")

    crs = sub.add_parser("validate-crs", help="Validate a dataset CRS")
    crs.add_argument("input")
    crs.add_argument("--expected")

    reproj = sub.add_parser("reproject", help="Reproject a vector dataset")
    reproj.add_argument("input")
    reproj.add_argument("output")
    reproj.add_argument("--crs", required=True)

    clip = sub.add_parser("clip", help="Clip a vector layer with a mask")
    clip.add_argument("input")
    clip.add_argument("mask")
    clip.add_argument("output")

    merge = sub.add_parser("merge", help="Merge multiple vector datasets")
    merge.add_argument("inputs", nargs="+")
    merge.add_argument("--output", required=True)

    return p


def main() -> None:
    args = build_parser().parse_args()
    gp = GeoProcessor()
    if args.command == "metadata":
        print(json.dumps(gp.metadata(args.input), indent=2, default=str))
    elif args.command == "validate-crs":
        gdf = read_vector(args.input)
        print(json.dumps(gp.validate_crs(gdf, args.expected), indent=2, default=str))
    elif args.command == "reproject":
        gdf = read_vector(args.input)
        out = gp.reproject_vector(gdf, args.crs)
        write_vector(out, args.output)
        gp.save_log()
    elif args.command == "clip":
        gdf = read_vector(args.input)
        mask = read_vector(args.mask)
        out = gp.clip_vector(gdf, mask)
        write_vector(out, args.output)
        gp.save_log()
    elif args.command == "merge":
        gdfs = [read_vector(p) for p in args.inputs]
        out = gp.merge_vectors(gdfs)
        write_vector(out, args.output)
        gp.save_log()


if __name__ == "__main__":
    main()
