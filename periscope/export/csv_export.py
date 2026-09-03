"""Write a canonical dataset to CSV."""

from __future__ import annotations

import csv
from pathlib import Path

from periscope.datasets.canonicalize import CANONICAL_COLUMNS, CanonicalDataset


def write_canonical_csv(dataset: CanonicalDataset, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(CANONICAL_COLUMNS))
        writer.writeheader()
        for row in dataset.rows:
            writer.writerow({col: row.get(col, "") for col in CANONICAL_COLUMNS})
    return path
