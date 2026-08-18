from pathlib import Path
import numpy as np
import geopandas as gpd
import rasterio
from rasterio.transform import from_origin
from shapely.geometry import Point, Polygon, LineString

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "sample_data"
DATA.mkdir(exist_ok=True)
CRS = "EPSG:4326"

# Facilities
facilities = gpd.GeoDataFrame({
    "facility": ["A", "B", "C", "D"],
    "type": ["hospital", "school", "hospital", "school"],
    "geometry": [Point(77.58, 12.96), Point(77.60, 12.975), Point(77.56, 12.99), Point(77.62, 12.95)],
}, crs=CRS)
facilities.to_file(DATA / "facilities.geojson", driver="GeoJSON")

# Zones
zones = gpd.GeoDataFrame({
    "zone": ["North", "South"],
    "priority": [2, 1],
    "geometry": [Polygon([(77.53, 12.98),(77.64,12.98),(77.64,13.02),(77.53,13.02)]), Polygon([(77.53,12.94),(77.64,12.94),(77.64,12.98),(77.53,12.98)])]
}, crs=CRS)
zones.to_file(DATA / "zones.geojson", driver="GeoJSON")

# Roads
roads = gpd.GeoDataFrame({
    "road_id": [1,2,3,4,5],
    "geometry": [
        LineString([(77.58,12.98),(77.53,12.98)]),
        LineString([(77.58,12.98),(77.64,12.98)]),
        LineString([(77.58,12.98),(77.58,12.93)]),
        LineString([(77.58,12.98),(77.58,13.03)]),
        LineString([(77.58,12.98),(77.64,13.02)]),
    ]
}, crs=CRS)
roads.to_file(DATA / "roads.geojson", driver="GeoJSON")

# Parcels
polys = []
land_value = []
road_distance = []
elevation = []
parcel_id = []
for i in range(4):
    for j in range(4):
        x0, y0 = 77.54 + i*0.024, 12.94 + j*0.02
        polys.append(Polygon([(x0,y0),(x0+0.02,y0),(x0+0.02,y0+0.016),(x0,y0+0.016)]))
        parcel_id.append(i*4+j+1)
        land_value.append(40 + 10*i + 3*j)
        road_distance.append(0.002 + 0.002*((i+j)%4))
        elevation.append(890 + 5*i - 2*j)
parcels = gpd.GeoDataFrame({"parcel_id":parcel_id,"land_value":land_value,"road_distance":road_distance,"elevation":elevation,"geometry":polys}, crs=CRS)
parcels.to_file(DATA / "parcels.geojson", driver="GeoJSON")

# Synthetic DEM
width = height = 60
xres = yres = 0.001
transform = from_origin(77.53, 13.03, xres, yres)
y, x = np.mgrid[0:height, 0:width]
dem = (900 + 0.7*x + 0.4*y + 12*np.sin(x/8) + 8*np.cos(y/10)).astype("float32")
profile = {"driver":"GTiff","height":height,"width":width,"count":1,"dtype":"float32","crs":CRS,"transform":transform,"nodata":-9999.0}
with rasterio.open(DATA / "dem.tif", "w", **profile) as dst:
    dst.write(dem, 1)

# Batch inputs: repeated versions of a small layer to demonstrate batch processing.
batch_dir = DATA / "batch_inputs"
batch_dir.mkdir(exist_ok=True)
for k in range(1, 4):
    batch = facilities.copy()
    batch["batch_id"] = k
    batch.to_file(batch_dir / f"facilities_batch_{k}.geojson", driver="GeoJSON")

print(f"Sample data written to {DATA}")
