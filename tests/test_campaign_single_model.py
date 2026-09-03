from __future__ import annotations

from periscope.campaign.runner import run_campaign
from periscope.measurement.simulated import SimulatedMeasurementClient


def test_single_arm_campaign_produces_expected_observation_count(single_arm_campaign_path):
    client = SimulatedMeasurementClient()
    result = run_campaign(single_arm_campaign_path, client=client, simulated=True)

    # 3 prompts x 1 arm x 3 repetitions
    assert result.canonical_dataset.observation_count == 9
    assert result.canonical_dataset.error_count == 0
    assert result.manifest.simulated is True
    assert result.manifest.arms == ["openai:gpt-4o-2024-11-20"]


def test_single_arm_campaign_writes_output_files(single_arm_campaign_path):
    client = SimulatedMeasurementClient()
    result = run_campaign(single_arm_campaign_path, client=client, simulated=True)

    assert (result.output_dir / "campaign_results.json").exists()
    assert (result.output_dir / "campaign_results.csv").exists()
    assert (result.output_dir / "campaign_manifest.json").exists()


def test_single_arm_campaign_rows_have_expected_signals(single_arm_campaign_path):
    client = SimulatedMeasurementClient()
    result = run_campaign(single_arm_campaign_path, client=client, simulated=True)

    row = result.canonical_dataset.rows[0]
    assert row["nm_stability_score"] is not None
    assert 0.0 <= row["nm_stability_score"] <= 1.0
    assert row["nm_schema_version"] == "0.2.0"
    assert row["op_latency_ms"] is not None
    assert row["op_token_count"] is not None
