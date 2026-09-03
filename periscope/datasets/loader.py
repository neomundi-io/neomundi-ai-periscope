"""Load a prompt corpus from CSV or JSON into a list of PromptRecord.

A dataset is the unit a campaign is run against. It is not a NeoMundi
concept -- it is defined entirely by the Periscope user.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PromptRecord:
    prompt_id: str
    prompt: str
    prompt_family: str = ""
    domain: str = ""


class DatasetError(ValueError):
    pass


def _row_to_prompt(row: dict, index: int) -> PromptRecord:
    prompt = row.get("prompt") or row.get("input") or row.get("question")
    if not prompt or not str(prompt).strip():
        raise DatasetError(f"Row {index}: missing 'prompt' field.")
    prompt_id = str(row.get("prompt_id") or row.get("id") or f"p{index:04d}")
    return PromptRecord(
        prompt_id=prompt_id,
        prompt=str(prompt).strip(),
        prompt_family=str(row.get("prompt_family") or row.get("family") or ""),
        domain=str(row.get("domain") or ""),
    )


def load_dataset(path: str | Path) -> list[PromptRecord]:
    """Load a CSV or JSON dataset of prompts.

    CSV columns: prompt_id (optional), prompt (required), prompt_family
    (optional), domain (optional).

    JSON: either a list of objects with the same fields, or an object with a
    'prompts' key holding that list.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
    elif suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            rows = data
        elif isinstance(data, dict) and isinstance(data.get("prompts"), list):
            rows = data["prompts"]
        else:
            raise DatasetError(
                "Unsupported JSON dataset structure: expected a list or an "
                "object with a 'prompts' list."
            )
    else:
        raise DatasetError(f"Unsupported dataset format: {suffix}. Use .csv or .json.")

    if not rows:
        raise DatasetError(f"Dataset is empty: {path}")

    return [_row_to_prompt(row, i) for i, row in enumerate(rows, start=1)]
