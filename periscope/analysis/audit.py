"""run_audit(): turn measured signals into review-priority objects.

This is a Periscope-side, descriptive prioritization heuristic -- not a
NeoMundi signal, not a verdict, and not an official NeoMundi threshold.
CONSUMER_BOUNDARIES.md is explicit that NeoMundi publishes no official
numeric thresholds; any threshold applied here is a Periscope campaign
configuration choice, and every AuditFinding carries that disclaimer plus
the measurement/normalizer versions it was computed against, per the same
document's guidance on what a consumer-defined threshold must record.

The default thresholds below are carried over, as a starting point only,
from the methodological reference (the private Euria/Fatima reporting
generator's HIGH_REVIEW/REVIEW/ROUTINE heuristic). They are not validated
NeoMundi norms and should be tuned per campaign.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from periscope.analysis._util import group_rows, numeric_values, stats
from periscope.datasets.canonicalize import CanonicalDataset
from periscope.measurement.contracts import NO_OFFICIAL_THRESHOLDS_NOTICE

REVIEW_PRIORITY_LABEL = "Periscope-derived review priority (descriptive heuristic, not a NeoMundi verdict)"


@dataclass(frozen=True)
class AuditThresholds:
    flag_rate_high: float = 0.10
    flag_rate_review: float = 0.0
    factual_risk_high: float = 0.05
    factual_risk_review: float = 0.01
    semantic_instability_high: float = 0.05
    semantic_instability_review: float = 0.01


DEFAULT_THRESHOLDS = AuditThresholds()


@dataclass
class AuditFinding:
    scope: str  # e.g. "arm:openai:gpt-4o" or "prompt:p0001"
    observation_count: int
    flag_rate: float | None
    factual_hallucination_mean: float | None
    semantic_instability_mean: float | None
    error_count: int
    review_priority: str  # "HIGH_REVIEW" | "REVIEW" | "ROUTINE"
    interpretation_boundary: str = REVIEW_PRIORITY_LABEL


@dataclass
class AuditReport:
    campaign_id: str
    thresholds: AuditThresholds
    thresholds_notice: str
    findings: list[AuditFinding] = field(default_factory=list)
    measurement_schema_versions: list[str] = field(default_factory=list)
    measurement_engine_versions: list[str] = field(default_factory=list)


def _priority(flag_rate: float | None, factual_mean: float | None, semantic_mean: float | None, t: AuditThresholds) -> str:
    flag_rate = flag_rate or 0.0
    factual_mean = factual_mean or 0.0
    semantic_mean = semantic_mean or 0.0

    if flag_rate >= t.flag_rate_high or factual_mean >= t.factual_risk_high or semantic_mean >= t.semantic_instability_high:
        return "HIGH_REVIEW"
    if flag_rate > t.flag_rate_review or factual_mean >= t.factual_risk_review or semantic_mean >= t.semantic_instability_review:
        return "REVIEW"
    return "ROUTINE"


def run_audit(dataset: CanonicalDataset, thresholds: AuditThresholds = DEFAULT_THRESHOLDS) -> AuditReport:
    by_arm = group_rows(dataset.rows, lambda r: r["id_arm_id"])

    findings = []
    for arm_id, rows in by_arm.items():
        decisions = [str(r.get("nm_decision") or "").upper() for r in rows]
        usable_decisions = [d for d in decisions if d]
        flag_rate = (sum(1 for d in usable_decisions if d == "FLAG") / len(usable_decisions)) if usable_decisions else None

        factual_mean = stats(numeric_values(rows, "nm_factual_hallucination_score"))["mean"]
        semantic_mean = stats(numeric_values(rows, "nm_semantic_instability_score"))["mean"]
        error_count = sum(1 for r in rows if r.get("op_error"))

        findings.append(
            AuditFinding(
                scope=f"arm:{arm_id}",
                observation_count=len(rows),
                flag_rate=flag_rate,
                factual_hallucination_mean=factual_mean,
                semantic_instability_mean=semantic_mean,
                error_count=error_count,
                review_priority=_priority(flag_rate, factual_mean, semantic_mean, thresholds),
            )
        )

    findings.sort(key=lambda f: {"HIGH_REVIEW": 0, "REVIEW": 1, "ROUTINE": 2}[f.review_priority])

    schema_versions = sorted({str(r["nm_schema_version"]) for r in dataset.rows if r.get("nm_schema_version")})
    engine_versions = sorted({str(r["nm_measurement_version"]) for r in dataset.rows if r.get("nm_measurement_version")})

    return AuditReport(
        campaign_id=dataset.campaign_id,
        thresholds=thresholds,
        thresholds_notice=NO_OFFICIAL_THRESHOLDS_NOTICE,
        findings=findings,
        measurement_schema_versions=schema_versions,
        measurement_engine_versions=engine_versions,
    )
