from __future__ import annotations

from pathlib import Path
from typing import Callable


def batch_process(input_dir: str | Path, output_dir: str | Path, processor: Callable[[Path, Path], None], pattern: str = "*.geojson") -> list[str]:
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    completed = []
    for src in sorted(input_dir.glob(pattern)):
        dst = output_dir / src.name
        processor(src, dst)
        completed.append(str(dst))
    return completed
