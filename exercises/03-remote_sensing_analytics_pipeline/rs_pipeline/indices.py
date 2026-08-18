"""Spectral index calculations."""
from __future__ import annotations
import numpy as np

def _normalised_difference(a, b):
    denom = a + b
    out = np.full_like(a, np.nan, dtype="float32")
    np.divide(a - b, denom, out=out, where=denom != 0)
    return out.astype("float32")

def ndvi(red, nir):
    """NDVI = (NIR - Red) / (NIR + Red)."""
    return _normalised_difference(nir, red)

def ndwi(green, nir):
    """NDWI = (Green - NIR) / (Green + NIR)."""
    return _normalised_difference(green, nir)
