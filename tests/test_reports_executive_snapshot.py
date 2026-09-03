from __future__ import annotations

import pytest

from periscope.campaign.runner import run_campaign
from periscope.measurement.simulated import SimulatedMeasurementClient
from periscope.reports.open.executive_snapshot import generate_executive_snapshot


@pytest.fixture
def campaign_result(two_model_campaign_path):
    client = SimulatedMeasurementClient()
    return run_campaign(two_model_campaign_path, client=client, simulated=True)


@pytest.mark.parametrize("lang", ["en", "fr"])
def test_executive_snapshot_html_generation(campaign_result, tmp_path, lang):
    result = generate_executive_snapshot(
        campaign_result.canonical_dataset,
        campaign_result.manifest,
        output_dir=tmp_path / "reports",
        lang=lang,
        render_pdf=False,
    )
    assert result.html_path.exists()
    content = result.html_path.read_text(encoding="utf-8")
    assert "None" not in content
    assert "Measured signal" in content or "Signal mesuré" in content
    assert campaign_result.manifest.campaign_id in content


def test_executive_snapshot_pdf_generation(campaign_result, tmp_path):
    result = generate_executive_snapshot(
        campaign_result.canonical_dataset,
        campaign_result.manifest,
        output_dir=tmp_path / "reports",
        lang="en",
        render_pdf=True,
    )
    assert result.html_path.exists()
    # PDF generation depends on an optional engine (playwright/weasyprint)
    # being installed; when available it must succeed, otherwise the
    # generator must degrade gracefully rather than raise.
    if result.pdf_path is not None:
        assert result.pdf_path.exists()
        assert result.pdf_path.stat().st_size > 0


def test_executive_snapshot_never_declares_verdicts(campaign_result, tmp_path):
    result = generate_executive_snapshot(
        campaign_result.canonical_dataset,
        campaign_result.manifest,
        output_dir=tmp_path / "reports",
        lang="en",
        render_pdf=False,
    )
    content = result.html_path.read_text(encoding="utf-8").lower()
    for forbidden in ("certified", "compliant", "non-compliant", "is the best model", "is unsafe", "is safe"):
        assert forbidden not in content
