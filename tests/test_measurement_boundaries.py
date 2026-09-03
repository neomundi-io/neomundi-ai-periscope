"""A missing/partial NeoMundi signal must surface as None everywhere it
flows through the system -- never silently converted to 0, "safe", or
"within_bounds". See docs/METRIC_BOUNDARIES.md and CONSUMER_BOUNDARIES.md.
"""

from __future__ import annotations

from periscope.analysis._util import stats
from periscope.campaign.runner import run_campaign
from periscope.measurement.contracts import (
    MeasurementRecord,
    ObservedSignal,
    SignalStatus,
    validate_coverage_consistency,
    validate_schema_version,
)
from periscope.measurement.runtime import build_measurement_record
from periscope.measurement.simulated import SimulatedMeasurementClient
import pytest


def test_fully_partial_campaign_never_invents_zero(single_arm_campaign_path):
    client = SimulatedMeasurementClient(partial_rate=1.0)  # every signal comes back unmeasured
    result = run_campaign(single_arm_campaign_path, client=client, simulated=True)

    for row in result.canonical_dataset.rows:
        assert row["nm_stability_score"] is None
        assert row["nm_stability_score_status"] in (SignalStatus.NOT_MEASURED.value, SignalStatus.INSUFFICIENT_COVERAGE.value)
        assert row["nm_measurement_status"] == "partial"
        assert row["nm_measurement_coverage"] == 0.0


def test_stats_over_all_missing_values_returns_none_not_zero():
    result = stats([])
    assert result["mean"] is None
    assert result["count"] is None


def test_v01_response_without_signal_status_infers_not_measured():
    # RGC v0.1 has no explicit signal_status; a missing field must be
    # inferred as not_measured, never as 0.0.
    raw = {
        "request_id": "req_1",
        "identity": {"schema_version": "0.1.0"},
        "quality": {"stability_score": 0.91},
        # coherence_score deliberately absent
    }
    record = build_measurement_record(raw)
    assert record.signal_value("stability_score") == 0.91
    assert record.signal_value("coherence_score") is None
    assert record.signals["coherence_score"].status == SignalStatus.NOT_MEASURED


def test_v02_signal_status_overrides_presence():
    # Even if a numeric value is present, an explicit non-"measured" status
    # must make it unusable -- status governs, not presence.
    raw = {
        "request_id": "req_2",
        "identity": {"schema_version": "0.2.0"},
        "observation": {
            "observed_signals": {
                "stability_score": 0.5,
                "signal_status": {"stability_score": "insufficient_coverage"},
            }
        },
    }
    record = build_measurement_record(raw)
    assert record.signal_value("stability_score") is None
    assert record.signals["stability_score"].status == SignalStatus.INSUFFICIENT_COVERAGE


def test_validate_schema_version_rejects_missing_and_unknown():
    with pytest.raises(ValueError):
        validate_schema_version(None)
    with pytest.raises(ValueError):
        validate_schema_version("9.9.9")
    validate_schema_version("0.2.0")  # does not raise


def test_validate_coverage_consistency_rejects_contradiction():
    with pytest.raises(ValueError):
        validate_coverage_consistency("complete", 0.8)
    with pytest.raises(ValueError):
        validate_coverage_consistency("partial", 1.0)
    validate_coverage_consistency("complete", 1.0)  # does not raise
    validate_coverage_consistency("partial", 0.6)  # does not raise
