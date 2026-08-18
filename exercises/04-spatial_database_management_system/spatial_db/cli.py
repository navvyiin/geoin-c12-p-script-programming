from __future__ import annotations

import argparse
from pathlib import Path

from .core import SpatialDatabaseApp


def main():
    parser = argparse.ArgumentParser(description="Spatial Database Management System")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="create an empty GeoPackage database path")
    init.add_argument("--db", default="outputs/spatial_database.gpkg")

    imp = sub.add_parser("import", help="import a vector dataset into a layer")
    imp.add_argument("source")
    imp.add_argument("--layer", required=True)
    imp.add_argument("--db", default="outputs/spatial_database.gpkg")

    sub.add_parser("layers", help="list database layers").add_argument(
        "--db", default="outputs/spatial_database.gpkg"
    )

    summary = sub.add_parser("summary", help="generate database summary reports")
    summary.add_argument("--db", default="outputs/spatial_database.gpkg")
    summary.add_argument("--output-dir", default="outputs")

    attr = sub.add_parser("attribute-query", help="run an attribute query")
    attr.add_argument("--db", default="outputs/spatial_database.gpkg")
    attr.add_argument("--layer", required=True)
    attr.add_argument("--column", required=True)
    attr.add_argument("--operator", required=True)
    attr.add_argument("--value", required=True)
    attr.add_argument("--output")

    spatial = sub.add_parser("intersects", help="select features intersecting another layer")
    spatial.add_argument("--db", default="outputs/spatial_database.gpkg")
    spatial.add_argument("--layer", required=True)
    spatial.add_argument("--mask", required=True)
    spatial.add_argument("--output")

    args = parser.parse_args()

    if args.command == "init":
        app = SpatialDatabaseApp(args.db)
        app.db_path.touch()
        print(f"Database path initialised: {app.db_path.resolve()}")
        return

    app = SpatialDatabaseApp(args.db)

    if args.command == "import":
        count = app.import_dataset(args.source, args.layer)
        print(f"Imported {count} features into layer '{args.layer}'.")
    elif args.command == "layers":
        for layer in app.layers():
            print(layer)
    elif args.command == "summary":
        payload = app.summary(args.output_dir)
        print(f"Layers: {len(payload['layers'])}")
        print(f"Summary report: {Path(args.output_dir).resolve()}")
    elif args.command == "attribute-query":
        value = float(args.value) if args.value.replace(".", "", 1).isdigit() else args.value
        result = app.query_attribute(args.layer, args.column, args.operator, value)
        print(f"Matched features: {len(result)}")
        if args.output:
            app.export(result, args.output)
            print(f"Exported: {Path(args.output).resolve()}")
    elif args.command == "intersects":
        result = app.query_intersection(args.layer, args.mask)
        print(f"Matched features: {len(result)}")
        if args.output:
            app.export(result, args.output)
            print(f"Exported: {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
