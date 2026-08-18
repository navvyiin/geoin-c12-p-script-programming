from __future__ import annotations

from sqlalchemy import create_engine, text


def build_postgis_engine(connection_url: str):
    """Create a SQLAlchemy engine for PostgreSQL/PostGIS."""
    return create_engine(connection_url, future=True)


def test_postgis_connection(connection_url: str) -> dict:
    """Run an introductory PostGIS connection test."""
    engine = build_postgis_engine(connection_url)
    with engine.connect() as conn:
        pg_version = conn.execute(text("SELECT version()")).scalar_one()
        try:
            postgis_version = conn.execute(
                text("SELECT PostGIS_Full_Version()")
            ).scalar_one()
        except Exception:
            postgis_version = None
    return {
        "connected": True,
        "postgresql_version": pg_version,
        "postgis_version": postgis_version,
    }
