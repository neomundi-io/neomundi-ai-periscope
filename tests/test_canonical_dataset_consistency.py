from __future__ import annotations

from periscope.campaign.runner import run_campaign
from periscope.datasets.canonicalize import CANONICAL_COLUMNS
from periscope.export.json_export import load_canonical_json, write_canonical_json
from periscope.measurement.simulated import SimulatedMeasurementClient


def test_canonical_rows_have_exactly_the_declared_columns(single_arm_campaign_path):
    client = SimulatedMeasurementClient()
    result = run_campaign(single_arm_campaign_path, client=client, simulated=True)

    for row in result.canonical_dataset.rows:
        assert set(row.keys()) == set(CANONICAL_COLUMNS)


def test_payload_hash_is_deterministic_for_same_rows(single_arm_campaign_path):
    client = SimulatedMeasurementClient()
    result = run_campaign(single_arm_campaign_path, client=client, simulated=True)

    hash_1 = result.canonical_dataset.payload_hash()
    hash_2 = result.canonical_dataset.payload_hash()
    assert hash_1 == hash_2
    assert len(hash_1) == 64  # sha256 hex digest


def test_payload_hash_changes_if_rows_change(single_arm_campaign_path):
    client = SimulatedMeasurementClient()
    result = run_campaign(single_arm_campaign_path, client=client, simulated=True)

    original_hash = result.canonical_dataset.payload_hash()
    mutated_rows = [dict(r) for r in result.canonical_dataset.rows]
    mutated_rows[0]["nm_stability_score"] = 0.0
    from periscope.datasets.canonicalize import CanonicalDataset

    mutated = CanonicalDataset(campaign_id=result.canonical_dataset.campaign_id, rows=mutated_rows)
    assert mutated.payload_hash() != original_hash


def test_json_round_trip_preserves_rows(single_arm_campaign_path, tmp_path):
    client = SimulatedMeasurementClient()
    result = run_campaign(single_arm_campaign_path, client=client, simulated=True)

    path = tmp_path / "roundtrip.json"
    write_canonical_json(result.canonical_dataset, path)
    reloaded = load_canonical_json(path)

    assert reloaded.campaign_id == result.canonical_dataset.campaign_id
    assert reloaded.payload_hash() == result.canonical_dataset.payload_hash()
    assert reloaded.observation_count == result.canonical_dataset.observation_count


def test_repetitions_are_deterministic_but_distinguishable(single_arm_campaign_path):
    """Repeated runs of the offline simulator against the same prompt/arm are
    deterministic per (prompt, arm, repetition) seed, but distinct
    repetitions of the same prompt are not forced to be identical --
    otherwise repeatability/variability analysis would be meaningless."""
    client = SimulatedMeasurementClient()
    result = run_campaign(single_arm_campaign_path, client=client, simulated=True)

    p001_rows = [r for r in result.canonical_dataset.rows if r["id_prompt_id"] == "p001"]
    assert len(p001_rows) == 3
    stability_values = {r["nm_stability_score"] for r in p001_rows}
    assert len(stability_values) > 1  # repetitions are not all identical
