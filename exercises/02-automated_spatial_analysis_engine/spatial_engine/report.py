from __future__ import annotations

from pathlib import Path
from typing import Any

from .utils import save_json


def build_report(results: dict[str, Any], markdown_path: str | Path, json_path: str | Path) -> None:
    markdown = [
        "# Automated Spatial Analysis Engine – Technical Report",
        "",
        "## Workflow summary",
        "",
        "| Operation | Result |",
        "|---|---|",
    ]
    for key, value in results.items():
        if isinstance(value, (dict, list)):
            display = str(value)
        else:
            display = str(value)
        markdown.append(f"| {key} | {display} |")
    markdown += [
        "",
        "## Manual versus automated workflow",
        "",
        "Manual GIS typically requires repeated layer loading, parameter entry, tool execution, intermediate-file management and quality checks. The automated workflow centralises these parameters in Python, records the sequence, reduces repetitive interaction, and produces reproducible outputs.",
        "",
        "## Reproducibility note",
        "",
        "The demonstration uses synthetic datasets and deterministic parameters. The same workflow can be applied to real vector and raster datasets by changing the input paths and analysis configuration.",
    ]
    Path(markdown_path).write_text("\n".join(markdown) + "\n", encoding="utf-8")
    save_json(results, json_path)
