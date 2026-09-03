"""NeoMundi measurements, Periscope campaign/operational data, and
Periscope-derived analysis must never collapse into one undifferentiated
blob. See docs/METRIC_BOUNDARIES.md.
"""

from __future__ import annotations

from periscope.analysis.audit import run_audit
from periscope.analysis.baseline import build_baseline
from periscope.analysis.comparison import compare_models
from periscope.campaign.runner import run_campaign
from periscope.datasets.canonicalize import CANONICAL_COLUMNS
from periscope.measurement.contracts import (
    CAMPAIGN_OPERATIONAL_FIELDS,
    NEOMUNDI_SIGNAL_FIELDS,
    classify_field,
)
from periscope.measurement.simulated import SimulatedMeasurementClient


def test_every_neomundi_signal_field_classifies_as_measurement():
    for name in NEOMUNDI_SIGNAL_FIELDS:
        assert classify_field(name) == "neomundi_measurement"


def test_every_campaign_operational_field_classifies_distinctly():
    for name in CAMPAIGN_OPERATIONAL_FIELDS:
        origin = classify_field(name)
        assert origin == "campaign_operational"
        assert origin != "neomundi_measurement"


def test_derived_analysis_vocabulary_is_absent_from_the_classifier():
    # "review_priority", "spread", "delta" etc. are Periscope-derived output
    # field names -- they must not be classifiable as measurement or
    # operational data, because they must never appear on a canonical row.
    for derived_name in ("review_priority", "spread", "delta_absolute", "benchmark_rank"):
        assert classify_field(derived_name) == "unknown"


def test_canonical_columns_only_cover_identifier_measurement_and_operational_namespaces():
    for column in CANONICAL_COLUMNS:
        assert column.startswith(("id_", "nm_", "op_")), f"Column {column} escapes the id_/nm_/op_ namespace convention."


def test_analysis_outputs_never_leak_into_canonical_dataset(single_arm_campaign_path):
    client = SimulatedMeasurementClient()
    result = run_campaign(single_arm_campaign_path, client=client, simulated=True)

    baseline = build_baseline(result.canonical_dataset)
    audit = run_audit(result.canonical_dataset)

    # Analysis results are separate dataclasses with their own field names
    # (e.g. "review_priority", "distribution") -- confirm none of those
    # derived field names were written back into the canonical rows.
    derived_field_names = {"review_priority", "distribution", "interpretation_boundary", "flag_rate"}
    for row in result.canonical_dataset.rows:
        assert derived_field_names.isdisjoint(row.keys())

    assert baseline.campaign_id == result.canonical_dataset.campaign_id
    assert audit.campaign_id == result.canonical_dataset.campaign_id
    assert audit.findings  # produced, but as a separate structure


def test_comparison_reference_group_is_explicit_not_a_ranking(single_arm_campaign_path):
    client = SimulatedMeasurementClient()
    result = run_campaign(single_arm_campaign_path, client=client, simulated=True)

    comparison = compare_models(result.canonical_dataset)
    # A single-arm campaign has exactly one "reference" group and no peer to
    # compare against -- comparison must not fabricate a ranking out of one point.
    assert comparison.reference_group is not None
    assert comparison.metrics[0].deltas == {}
