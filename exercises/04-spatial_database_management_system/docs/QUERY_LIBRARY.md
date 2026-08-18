# Query Library

The Python query library is implemented in `spatial_db/queries.py`.

## Attribute query

```python
app.query_attribute("places", "population", ">=", 8000)
```

## Spatial intersection

```python
app.query_intersection("places", "zones")
```

## Spatial within

```python
app.query_within("places", "zones")
```

## Nearest distance

```python
app.query_nearest("places", "zones")
```

## Introductory PostGIS SQL

```sql
SELECT p.name, p.population
FROM places AS p
WHERE p.population >= 8000;

SELECT p.name, z.zone_name
FROM places AS p
JOIN zones AS z
  ON ST_Intersects(p.geometry, z.geometry);

SELECT p.name, ST_Distance(p.geometry::geography, z.geometry::geography)
FROM places AS p
CROSS JOIN LATERAL (
    SELECT geometry FROM zones
    ORDER BY p.geometry <-> geometry
    LIMIT 1
) AS z;
```
