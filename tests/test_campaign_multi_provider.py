from __future__ import annotations

from periscope.analysis.comparison import compare_providers
from periscope.campaign.runner import run_campaign
from periscope.measurement.simulated import SimulatedMeasurementClient


def test_multi_provider_campaign_expands_correctly(multi_provider_campaign_path):
    client = SimulatedMeasurementClient()
    result = run_campaign(multi_provider_campaign_path, client=client, simulated=True)

    # 3 prompts x 3 arms x 2 repetitions
    assert result.canonical_dataset.observation_count == 18
    assert sorted(result.manifest.arms) == sorted(
        ["openai:gpt-4o-2024-11-20", "anthropic:claude-sonnet-5", "mistral:mistral-large"]
    )


def test_compare_providers_covers_all_three(multi_provider_campaign_path):
    client = SimulatedMeasurementClient()
    result = run_campaign(multi_provider_campaign_path, client=client, simulated=True)

    comparison = compare_providers(result.canonical_dataset)
    assert sorted(comparison.groups) == ["anthropic", "mistral", "openai"]
    for provider in comparison.groups:
        assert comparison.observation_counts[provider] == 6  # 3 prompts x 2 repetitions
