from __future__ import annotations

import pytest

from periscope.datasets.loader import DatasetError, load_dataset
from periscope.datasets.validation import require_valid, validate_dataset


def test_load_csv_dataset(dataset_path):
    records = load_dataset(dataset_path)
    assert len(records) == 3
    assert records[0].prompt_id == "p001"
    assert records[0].prompt.startswith("Explain one potential risk")


def test_load_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_dataset(tmp_path / "does_not_exist.csv")


def test_load_empty_dataset_raises(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("prompt_id,prompt\n", encoding="utf-8")
    with pytest.raises(DatasetError):
        load_dataset(path)


def test_validate_detects_duplicate_prompt_ids(tmp_path):
    path = tmp_path / "dupes.csv"
    path.write_text("prompt_id,prompt\np1,Hello\np1,World\n", encoding="utf-8")
    records = load_dataset(path)
    report = validate_dataset(records)
    assert not report.is_valid
    assert report.duplicate_prompt_ids == ["p1"]

    with pytest.raises(ValueError):
        require_valid(records)


def test_validate_passes_for_clean_dataset(dataset_path):
    records = load_dataset(dataset_path)
    report = require_valid(records)
    assert report.is_valid
    assert report.total == 3
