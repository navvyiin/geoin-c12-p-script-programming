"""Create deterministic synthetic multispectral scenes for teaching."""
from pathlib import Path
import numpy as np
import rasterio
from rasterio.transform import from_origin

def make_scene(path, seed, vegetation_shift=0):
    rng = np.random.default_rng(seed); h=w=120; yy,xx=np.mgrid[0:h,0:w]
    blue=np.full((h,w),0.12,dtype="float32"); green=np.full((h,w),0.16,dtype="float32"); red=np.full((h,w),0.20,dtype="float32"); nir=np.full((h,w),0.25,dtype="float32")
    water=((xx-28)**2+(yy-28)**2)<18**2
    vegetation=(((xx-78)**2+(yy-38)**2)<26**2)|(((xx-74)**2+(yy-78)**2)<(28+vegetation_shift)**2)
    built=(xx>70)&(yy<22); bare=(xx<45)&(yy>75)
    blue[water],green[water],red[water],nir[water]=0.06,0.10,0.05,0.03
    blue[vegetation],green[vegetation],red[vegetation],nir[vegetation]=0.06,0.18,0.05,0.42
    blue[built],green[built],red[built],nir[built]=0.20,0.23,0.25,0.28
    blue[bare],green[bare],red[bare],nir[bare]=0.24,0.26,0.31,0.35
    for arr in (blue,green,red,nir):
        arr += rng.normal(0,0.008,size=arr.shape).astype("float32"); np.clip(arr,0.001,0.95,out=arr)
    profile={"driver":"GTiff","height":h,"width":w,"count":4,"dtype":"float32","crs":"EPSG:32643","transform":from_origin(500000,1500000,10,10),"compress":"deflate"}
    path.parent.mkdir(parents=True,exist_ok=True)
    with rasterio.open(path,"w",**profile) as dst:
        for i,arr in enumerate((blue,green,red,nir),1): dst.write(arr, i)
if __name__=="__main__":
    out=Path(__file__).resolve().parents[1]/"sample_data"; make_scene(out/"scene_2023.tif",11,0); make_scene(out/"scene_2024.tif",22,10); print("Sample Earth observation scenes created.")
