# Technical Report

## Objective
Develop a reproducible Python-based Earth observation workflow using multispectral imagery.

## Processing chain
1. Read four-band multispectral GeoTIFF imagery.
2. Compute NDVI and NDWI.
3. Perform introductory Random Forest image classification.
4. Calculate land-cover area statistics.
5. Detect basic land-cover changes between two scenes.
6. Export thematic maps and summary statistics.
7. Generate a scientific report.

## Scientific note
The sample scenes are synthetic teaching datasets and should not be interpreted as real satellite observations. The workflow architecture is intended to be reusable with real multispectral GeoTIFF data after appropriate preprocessing and quality control.
