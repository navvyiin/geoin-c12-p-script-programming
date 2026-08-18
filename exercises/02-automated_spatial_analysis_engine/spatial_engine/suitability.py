from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
import pandas as pd


@dataclass
class SuitabilityCriterion:
    name: str
    weight: float
    direction: str = "benefit"


def minmax(values: pd.Series) -> pd.Series:
    v = values.astype(float)
    lo, hi = v.min(), v.max()
    if hi == lo:
        return pd.Series(np.ones(len(v)), index=v.index)
    return (v - lo) / (hi - lo)


def weighted_suitability(df: pd.DataFrame, criteria: Sequence[SuitabilityCriterion]) -> pd.DataFrame:
    out = df.copy()
    total = sum(c.weight for c in criteria)
    if total <= 0:
        raise ValueError("Criterion weights must sum to a positive value.")
    score = np.zeros(len(out), dtype=float)
    for c in criteria:
        if c.name not in out.columns:
            raise KeyError(f"Missing suitability field: {c.name}")
        norm = minmax(out[c.name])
        if c.direction == "cost":
            norm = 1.0 - norm
        elif c.direction != "benefit":
            raise ValueError("direction must be 'benefit' or 'cost'")
        out[f"norm_{c.name}"] = norm
        score += norm.to_numpy() * c.weight
    out["suitability_score"] = score / total
    out["suitability_rank"] = out["suitability_score"].rank(method="dense", ascending=False).astype(int)
    return out.sort_values("suitability_rank")
