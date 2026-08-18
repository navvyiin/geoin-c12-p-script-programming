"""Thematic map and composite export."""
from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def export_png(array, path, title, cmap="viridis"):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 6)); plt.imshow(array, cmap=cmap); plt.title(title); plt.axis("off"); plt.tight_layout(); plt.savefig(path, dpi=180, bbox_inches="tight"); plt.close()

def export_rgb_png(blue, green, red, path, title="False-colour composite"):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    rgb = np.stack([red, green, blue], axis=-1).astype("float32")
    lo = np.percentile(rgb, 2, axis=(0, 1), keepdims=True); hi = np.percentile(rgb, 98, axis=(0, 1), keepdims=True)
    rgb = np.clip((rgb - lo) / np.where(hi == lo, 1, hi - lo), 0, 1)
    plt.figure(figsize=(8, 6)); plt.imshow(rgb); plt.title(title); plt.axis("off"); plt.tight_layout(); plt.savefig(path, dpi=180, bbox_inches="tight"); plt.close()
