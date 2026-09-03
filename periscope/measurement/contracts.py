"""Vocabulary and structural rules for the NeoMundi measurement contract (RGC).

This module does not reimplement NeoMundi's measurement engine. It encodes only
the *field vocabulary* and *structural rules* needed to consume a NeoMundi
measurement record safely, per:

- NeoMundi Runtime Measurement Layer — docs/MEASUREMENT_CONTRACT.md, docs/CONSUMER_BOUNDARIES.md
- NeoMundi Metric Contract v0.0 (Draft)
- NeoMundi Measurement Interoperability Contract (RGC v0.1 / v0.2)

Full JSON Schema validation and cryptographic signature verification are the
responsibility of NeoMundi's published schemas and reference verifier
(see reference/NOTES.md). The checks here are structural and defensive, not a
replacement for that schema.

Boundary enforced throughout this package:

    NeoMundi measurement  !=  campaign operational data  !=  Periscope-derived analysis
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


SUPPORTED_SCHEMA_VERSIONS = ("0.1.0", "0.2.0")
"""RGC schema versions this build understands. Never interpret a contract
under a schema version it does not declare (see CONSUMER_BOUNDARIES.md,
"Match the schema version")."""


class SignalStatus(str, Enum):
    """Per-signal measurement status introduced in RGC v0.2.

    A ``measured`` signal must carry a numeric value. Any other status must
    carry ``null`` -- it must never be silently replaced by a reassuring
    default such as 0 or "safe".
    """

    MEASURED = "measured"
    NOT_MEASURED = "not_measured"
    INSUFFICIENT_COVERAGE = "insufficient_coverage"


class ObservationClass(str, Enum):
    WITHIN_BOUNDS = "within_bounds"
    FLAGGED = "flagged"
    NOT_ASSESSED = "not_assessed"  # RGC v0.2 only


class GovernanceDecision(str, Enum):
    """The `governance.decision` signal. A signal, not an executed action."""

    ALLOW = "ALLOW"
    FLAG = "FLAG"
    REROUTE = "REROUTE"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    STOP = "STOP"


# ---------------------------------------------------------------------------
# Field vocabulary
# ---------------------------------------------------------------------------

# Signals returned by NeoMundi's /v1/govern measurement response
# (quality / runtime / governance / observation.observed_signals blocks).
# These are NeoMundi measurements. Periscope must never recompute them
# differently or relabel them as its own analysis.
NEOMUNDI_SIGNAL_FIELDS = (
    "stability_score",
    "coherence_score",
    "factual_hallucination_score",   # aka factual_validity_signal in the Metric Contract
    "semantic_instability_score",    # aka semantic_variability_signal in the Metric Contract
    "semantic_risk",
    "confidence",
    "observation_class",
    "decision",                      # governance.decision — advisory signal, not an executed action
)

# Per-observation measurement metadata, also sourced from NeoMundi.
NEOMUNDI_OBSERVATION_META_FIELDS = (
    "schema_version",
    "measurement_version",
    "normalizer_version",
    "measurement_status",
    "measurement_coverage",
    "request_id",
    "trace_id",
)

# Data captured by the Periscope client itself while running the campaign
# (timing the call, counting tokens from the reconstructed response) and
# then submitted to NeoMundi as `raw_metrics` context for measurement.
# This is campaign operational data, NOT a NeoMundi-computed signal, even
# though it travels alongside the measurement record.
CAMPAIGN_OPERATIONAL_FIELDS = (
    "latency_ms",
    "token_count",
)

# Identifiers that describe the campaign/execution context, not a measurement.
CAMPAIGN_IDENTIFIER_FIELDS = (
    "campaign_id",
    "dataset_id",
    "prompt_id",
    "prompt_family",
    "domain",
    "provider",
    "model",
    "repetition_index",
    "planned_repetitions",
    "arm_id",
    "timestamp_utc",
)

FieldOrigin = str  # "neomundi_measurement" | "campaign_operational" | "campaign_identifier" | "unknown"


def classify_field(name: str) -> FieldOrigin:
    """Classify a canonical dataset column by its origin.

    This is the mechanism that keeps NeoMundi measurements and Periscope
    campaign/operational data structurally separated. Periscope-derived
    analysis (benchmark, baseline, audit...) is never written into the
    canonical observation row at all -- it lives in separate analysis
    output tables -- so it is intentionally absent from this classifier.
    """

    if name in NEOMUNDI_SIGNAL_FIELDS or name in NEOMUNDI_OBSERVATION_META_FIELDS:
        return "neomundi_measurement"
    if name in CAMPAIGN_OPERATIONAL_FIELDS:
        return "campaign_operational"
    if name in CAMPAIGN_IDENTIFIER_FIELDS:
        return "campaign_identifier"
    return "unknown"


@dataclass
class ObservedSignal:
    """A single NeoMundi signal, with its RGC v0.2 measurement status.

    Under v0.1 there is no explicit per-signal status; a present numeric
    value is treated as ``measured`` and a missing one as ``not_measured``.
    """

    name: str
    value: float | None
    status: SignalStatus

    def is_usable(self) -> bool:
        return self.status == SignalStatus.MEASURED and self.value is not None


@dataclass
class MeasurementRecord:
    """Normalized view of one NeoMundi measurement (RGC v0.1 or v0.2), as
    consumed by Periscope. Constructed by `measurement.runtime`, never by
    hand-editing a raw API response.
    """

    request_id: str | None
    schema_version: str | None
    measurement_version: str | None
    normalizer_version: str | None
    measurement_status: str | None
    measurement_coverage: float | None
    observation_class: str | None
    decision: str | None
    signals: dict[str, ObservedSignal] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    def signal_value(self, name: str) -> float | None:
        """Return a signal's numeric value only if it was actually measured.

        Never returns 0.0 or any other default for a missing/partial signal
        -- callers must treat `None` as "measurement unavailable".
        """
        sig = self.signals.get(name)
        return sig.value if sig and sig.is_usable() else None


def validate_schema_version(schema_version: str | None) -> None:
    """Reject an unrecognized or missing schema_version.

    Raises ValueError rather than guessing. Per CONSUMER_BOUNDARIES.md, a
    consumer must never silently validate a contract against the wrong
    schema version, and a malformed/unversioned payload must never be
    treated as a valid measurement.
    """
    if not schema_version:
        raise ValueError(
            "Missing identity.schema_version on a measurement record. "
            "A record without a declared schema version cannot be interpreted."
        )
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError(
            f"Unsupported RGC schema_version {schema_version!r}. "
            f"This build understands {SUPPORTED_SCHEMA_VERSIONS}."
        )


def validate_coverage_consistency(measurement_status: str | None, measurement_coverage: float | None) -> None:
    """RGC v0.2 normative rule: status=complete <=> coverage=1.0, status=partial <=> coverage<1.0.

    Only enforced when both fields are present (v0.1 records may not carry them).
    """
    if measurement_status is None or measurement_coverage is None:
        return
    if measurement_status == "complete" and measurement_coverage != 1.0:
        raise ValueError(
            f"Inconsistent measurement record: measurement_status=complete but "
            f"measurement_coverage={measurement_coverage} (expected 1.0)."
        )
    if measurement_status == "partial" and measurement_coverage >= 1.0:
        raise ValueError(
            "Inconsistent measurement record: measurement_status=partial but "
            "measurement_coverage is not < 1.0."
        )


NO_OFFICIAL_THRESHOLDS_NOTICE = (
    "NeoMundi does not publish official numeric thresholds for its signals. "
    "Any threshold used below is a Periscope-side, campaign-specific "
    "configuration choice -- not a NeoMundi norm. See docs/METRIC_BOUNDARIES.md."
)
