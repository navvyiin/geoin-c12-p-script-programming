"""Introductory supervised land-cover classification."""
from __future__ import annotations
import numpy as np
from sklearn.ensemble import RandomForestClassifier

CLASS_NAMES = {1: "Water", 2: "Vegetation", 3: "Built-up", 4: "Bare soil"}

def build_training_labels(blue, green, red, nir):
    ndvi = (nir - red) / np.where(nir + red == 0, 1, nir + red)
    ndwi = (green - nir) / np.where(green + nir == 0, 1, green + nir)
    labels = np.zeros_like(red, dtype="uint8")
    labels[(ndwi > 0.10) & (ndvi < 0.25)] = 1
    labels[ndvi >= 0.25] = 2
    remaining = labels == 0
    labels[remaining & (red > 0.22) & (nir < 0.36)] = 3
    labels[labels == 0] = 4
    return labels

def train_classifier(blue, green, red, nir, labels, random_state=42):
    X = np.column_stack([blue.ravel(), green.ravel(), red.ravel(), nir.ravel()])
    y = labels.ravel()
    mask = y > 0
    if np.count_nonzero(mask) < 20:
        raise ValueError("Not enough labelled pixels for classification.")
    model = RandomForestClassifier(n_estimators=80, max_depth=12, random_state=random_state, n_jobs=-1)
    model.fit(X[mask], y[mask])
    return model

def classify_image(model, blue, green, red, nir):
    X = np.column_stack([blue.ravel(), green.ravel(), red.ravel(), nir.ravel()])
    return model.predict(X).reshape(red.shape).astype("uint8")
