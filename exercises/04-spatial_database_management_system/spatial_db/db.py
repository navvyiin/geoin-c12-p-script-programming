from __future__ import annotations

from pathlib import Path
import geopandas as gpd


DEFAULT_LAYERS = ("places", "zones")


def initialise_database(db_path: str | Path) -> Path:
    """Create the parent directory and return the GeoPackage path."""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def import_layer(db_path: str | Path, source_path: str | Path, layer_name: str) -> int:
    """Import a vector dataset into a GeoPackage layer."""
    db_path = initialise_database(db_path)
    gdf = gpd.read_file(source_path)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    gdf.to_file(db_path, layer=layer_name, driver="GPKG", mode="w")
    return len(gdf)


def read_layer(db_path: str | Path, layer_name: str) -> gpd.GeoDataFrame:
    """Read a GeoPackage layer."""
    return gpd.read_file(db_path, layer=layer_name)


def list_layers(db_path: str | Path) -> list[str]:
    """List available GeoPackage layers using Fiona."""
    import fiona
    return list(fiona.listlayers(db_path))


def update_layer(db_path: str | Path, layer_name: str, gdf: gpd.GeoDataFrame) -> None:
    """Replace a layer with an updated GeoDataFrame."""
    gdf.to_file(db_path, layer=layer_name, driver="GPKG", mode="w")


def export_layer(gdf: gpd.GeoDataFrame, output_path: str | Path, layer: str = "query_result") -> Path:
    """Export query results to GeoPackage or GeoJSON."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = output_path.suffix.lower()
    if suffix == ".geojson":
        gdf.to_file(output_path, driver="GeoJSON")
    elif suffix == ".gpkg":
        gdf.to_file(output_path, layer=layer, driver="GPKG", mode="w")
    else:
        raise ValueError("Supported export formats: .gpkg and .geojson")
    return output_path
