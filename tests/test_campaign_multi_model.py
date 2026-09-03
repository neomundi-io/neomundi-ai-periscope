from __future__ import annotations

from periscope.analysis.benchmark import build_benchmark
from periscope.analysis.comparison import compare_models
from periscope.campaign.runner import run_campaign
from periscope.measurement.simulated import SimulatedMeasurementClient


def test_two_model_campaign_expands_correctly(two_model_campaign_path):
    client = SimulatedMeasurementClient()
    result = run_campaign(two_model_campaign_path, client=client, simulated=True)

    # 3 prompts x 2 arms x 2 repetitions
    assert result.canonical_dataset.observation_count == 12
    assert sorted(result.manifest.arms) == ["openai:gpt-4o-2024-11-20", "openai:gpt-4o-mini"]


def test_compare_models_produces_deltas(two_model_campaign_path):
    client = SimulatedMeasurementClient()
    result = run_campaign(two_model_campaign_path, client=client, simulated=True)

    comparison = compare_models(result.canonical_dataset, reference_model="gpt-4o-2024-11-20")
    assert comparison.reference_group == "gpt-4o-2024-11-20"
    assert "gpt-4o-mini" in comparison.groups

    stability = next(m for m in comparison.metrics if m.metric == "nm_stability_score")
    assert "gpt-4o-mini_vs_gpt-4o-2024-11-20" in stability.deltas


def test_build_benchmark_uses_configured_baseline_arm(two_model_campaign_path):
    client = SimulatedMeasurementClient()
    result = run_campaign(two_model_campaign_path, client=client, simulated=True)

    benchmark = build_benchmark(result.canonical_dataset, reference_arm_id=result.manifest.baseline_arm_id)
    assert benchmark.reference_arm_id == "openai:gpt-4o-2024-11-20"
    assert benchmark.arm_comparison is not None
    assert len(benchmark.baselines_by_arm) == 2
    assert "not a universal leaderboard" in benchmark.notice.lower()
