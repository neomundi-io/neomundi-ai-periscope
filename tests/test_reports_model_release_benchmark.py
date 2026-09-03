from __future__ import annotations

import pytest

from periscope.campaign.runner import run_campaign
from periscope.measurement.simulated import SimulatedMeasurementClient
from periscope.reports.open.model_release_benchmark import generate_model_release_benchmark


@pytest.fixture
def campaign_result(two_model_campaign_path):
    client = SimulatedMeasurementClient()
    return run_campaign(two_model_campaign_path, client=client, simulated=True)


@pytest.mark.parametrize("lang", ["en", "fr"])
def test_benchmark_report_html_generation(campaign_result, tmp_path, lang):
    result = generate_model_release_benchmark(
        campaign_result.canonical_dataset,
        campaign_result.manifest,
        output_dir=tmp_path / "reports",
        lang=lang,
        reference_arm_id=campaign_result.manifest.baseline_arm_id,
        render_pdf=False,
    )
    assert result.html_path.exists()
    content = result.html_path.read_text(encoding="utf-8")
    assert "None" not in content
    assert "openai:gpt-4o-2024-11-20" in content
    assert "openai:gpt-4o-mini" in content


def test_benchmark_report_pdf_generation(campaign_result, tmp_path):
    result = generate_model_release_benchmark(
        campaign_result.canonical_dataset,
        campaign_result.manifest,
        output_dir=tmp_path / "reports",
        lang="en",
        render_pdf=True,
    )
    if result.pdf_path is not None:
        assert result.pdf_path.exists()
        assert result.pdf_path.stat().st_size > 0


def test_benchmark_report_is_not_a_leaderboard(campaign_result, tmp_path):
    result = generate_model_release_benchmark(
        campaign_result.canonical_dataset,
        campaign_result.manifest,
        output_dir=tmp_path / "reports",
        lang="en",
        render_pdf=False,
    )
    content = result.html_path.read_text(encoding="utf-8").lower()
    assert "not a universal leaderboard" in content
    assert "is the best model" not in content


def test_benchmark_report_reproducibility_manifest_section_has_hashes(campaign_result, tmp_path):
    result = generate_model_release_benchmark(
        campaign_result.canonical_dataset,
        campaign_result.manifest,
        output_dir=tmp_path / "reports",
        lang="en",
        render_pdf=False,
    )
    content = result.html_path.read_text(encoding="utf-8")
    assert campaign_result.canonical_dataset.payload_hash() in content
