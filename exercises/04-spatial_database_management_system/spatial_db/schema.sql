-- Introductory PostgreSQL/PostGIS schema
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS places (
    place_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    population INTEGER NOT NULL,
    category TEXT,
    geometry geometry(Point, 4326)
);

CREATE INDEX IF NOT EXISTS places_geometry_gix
    ON places USING GIST (geometry);

CREATE TABLE IF NOT EXISTS zones (
    zone_id INTEGER PRIMARY KEY,
    zone_name TEXT NOT NULL,
    priority INTEGER NOT NULL,
    geometry geometry(Polygon, 4326)
);

CREATE INDEX IF NOT EXISTS zones_geometry_gix
    ON zones USING GIST (geometry);
