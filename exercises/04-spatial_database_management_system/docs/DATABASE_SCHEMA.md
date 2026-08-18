# Database Schema

The local demonstration uses a GeoPackage database so it can run without a database server.

## `places`

| Field | Type | Description |
|---|---|---|
| `place_id` | Integer | Unique place identifier |
| `name` | Text | Place name |
| `population` | Integer | Estimated population |
| `category` | Text | Classification |
| `geometry` | Point | Spatial location |

## `zones`

| Field | Type | Description |
|---|---|---|
| `zone_id` | Integer | Unique zone identifier |
| `zone_name` | Text | Zone name |
| `priority` | Integer | Priority score |
| `geometry` | Polygon | Zone boundary |

The same conceptual schema can be migrated to PostgreSQL/PostGIS.
