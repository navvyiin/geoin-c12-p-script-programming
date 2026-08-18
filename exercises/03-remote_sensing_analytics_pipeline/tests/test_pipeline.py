import numpy as np
from affine import Affine
from rs_pipeline.change_detection import change_map, transition_matrix
from rs_pipeline.indices import ndvi, ndwi
from rs_pipeline.stats import area_statistics, raster_summary

def test_indices():
    red=np.array([[0.2,0.1]],dtype="float32"); nir=np.array([[0.6,0.4]],dtype="float32"); green=np.array([[0.3,0.2]],dtype="float32")
    assert np.allclose(ndvi(red,nir), [[0.5,0.6]], atol=1e-6)
    assert np.allclose(ndwi(green,nir), [[-0.33333334,-0.33333334]], atol=1e-6)

def test_change():
    before=np.array([[1,2],[3,4]],dtype="uint8"); after=np.array([[1,4],[3,4]],dtype="uint8")
    assert int(change_map(before,after).sum())==1; assert transition_matrix(before,after)["2->4"]==1

def test_statistics():
    arr=np.array([[1,1],[2,2]],dtype="uint8"); profile={"transform":Affine(10,0,0,0,-10,0)}; stats=area_statistics(arr,profile)
    assert len(stats)==2 and stats[0]["area_m2"]==200.0
    assert raster_summary(np.array([[1.0,3.0]],dtype="float32"))["mean"]==2.0
