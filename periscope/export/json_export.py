"""Write a canonical dataset to JSON."""

from __future__ import annotations

import json
from pathlib import Path

from periscope.datasets.canonicalize import CanonicalDataset


def write_canonical_json(dataset: CanonicalDataset, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "campaign_id": dataset.campaign_id,
        "observation_count": dataset.observation_count,
        "payload_hash": dataset.payload_hash(),
        "observations": dataset.rows,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_canonical_json(path: str | Path) -> CanonicalDataset:
    path = Path(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    return CanonicalDataset(campaign_id=payload["campaign_id"], rows=payload["observations"])
