"""run_evaluation(): a structured record of corpus, protocol, observations,
anomalies and limitations -- the backing data for the advanced Audit /
Evaluation Report (documented, not shipped as a public generator in this
build; see docs/REPORT_LIBRARY.md).

Kept deliberately close to the reproducibility fields the product commits
to (docs/PRODUCT_ARCHITECTURE.md): what corpus, how many executions, which
arms, which versions, when, what was excluded.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from periscope.analysis._util import group_rows
from periscope.datasets.canonicalize import CanonicalDataset
from periscope.export.manifest import CampaignManifest


@dataclass
class EvaluationSummary:
    campaign_id: str
    dataset_id: str
    arms: list[str]
    observation_count: int
    error_count: int
    error_rate: float | None
    flagged_count: int
    measurement_schema_versions: list[str]
    measurement_engine_versions: list[str]
    excluded_observations: list[dict] = field(default_factory=list)
    known_limitations: list[str] = field(default_factory=list)


DEFAULT_LIMITATIONS = (
    "Results apply only to the tested corpus, providers, models, repetitions "
    "and measurement versions recorded in the campaign manifest.",
    "A NeoMundi measurement is a runtime signal, not a verdict about truth, "
    "safety, legality, or business acceptability.",
    "Missing or partial NeoMundi signals are reported as unavailable, never "
    "as 0, 'safe', or 'within bounds'.",
    "Review-priority and other Periscope-derived heuristics are descriptive "
    "prioritization aids, not NeoMundi norms and not automated decisions.",
)


def run_evaluation(dataset: CanonicalDataset, manifest: CampaignManifest) -> EvaluationSummary:
    error_rows = [r for r in dataset.rows if r.get("op_error")]
    flagged_rows = [r for r in dataset.rows if str(r.get("nm_decision") or "").upper() == "FLAG"]

    excluded = [
        {
            "prompt_id": r["id_prompt_id"],
            "arm_id": r["id_arm_id"],
            "repetition_index": r["id_repetition_index"],
            "reason": r.get("op_error"),
        }
        for r in error_rows
    ]

    total = dataset.observation_count
    return EvaluationSummary(
        campaign_id=dataset.campaign_id,
        dataset_id=manifest.dataset_id,
        arms=manifest.arms,
        observation_count=total,
        error_count=len(error_rows),
        error_rate=(len(error_rows) / total) if total else None,
        flagged_count=len(flagged_rows),
        measurement_schema_versions=manifest.measurement_schema_versions,
        measurement_engine_versions=manifest.measurement_engine_versions,
        excluded_observations=excluded,
        known_limitations=list(DEFAULT_LIMITATIONS),
    )
