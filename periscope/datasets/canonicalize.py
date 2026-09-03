"""Build the canonical campaign dataset: one flat, hashable row per observation.

The canonical row keeps three namespaces strictly separate by column prefix:

- `id_*`  -- campaign/execution identifiers (not a measurement)
- `nm_*`  -- NeoMundi measurement fields (never recomputed by Periscope)
- `op_*`  -- campaign operational data captured by the Periscope client
             (latency, token count) -- NOT a NeoMundi signal

Periscope-derived analysis (benchmark, baseline, audit...) is never added to
this row. It is produced separately by `periscope.analysis.*` and stored in
its own output tables, so a canonical dataset on disk can never be mistaken
for an analysis result.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from periscope.measurement.contracts import MeasurementRecord, SignalStatus


@dataclass
class Observation:
    """One executed unit of a campaign: one prompt, one arm, one repetition."""

    campaign_id: str
    dataset_id: str
    prompt_id: str
    prompt: str
    prompt_family: str
    domain: str
    provider: str
    model: str
    arm_id: str
    repetition_index: int
    planned_repetitions: int
    timestamp_utc: str
    measurement: MeasurementRecord | None = None
    latency_ms: float | None = None
    token_count: int | None = None
    error: str | None = None


CANONICAL_ID_COLUMNS = (
    "id_campaign_id",
    "id_dataset_id",
    "id_prompt_id",
    "id_prompt_text",
    "id_prompt_family",
    "id_domain",
    "id_provider",
    "id_model",
    "id_arm_id",
    "id_repetition_index",
    "id_planned_repetitions",
    "id_timestamp_utc",
)

CANONICAL_NM_COLUMNS = (
    "nm_request_id",
    "nm_schema_version",
    "nm_measurement_version",
    "nm_normalizer_version",
    "nm_measurement_status",
    "nm_measurement_coverage",
    "nm_observation_class",
    "nm_decision",
    "nm_stability_score",
    "nm_stability_score_status",
    "nm_coherence_score",
    "nm_coherence_score_status",
    "nm_factual_hallucination_score",
    "nm_factual_hallucination_score_status",
    "nm_semantic_instability_score",
    "nm_semantic_instability_score_status",
    "nm_semantic_risk",
    "nm_semantic_risk_status",
    "nm_confidence",
    "nm_confidence_status",
)

CANONICAL_OP_COLUMNS = (
    "op_latency_ms",
    "op_token_count",
    "op_error",
)

CANONICAL_COLUMNS = CANONICAL_ID_COLUMNS + CANONICAL_NM_COLUMNS + CANONICAL_OP_COLUMNS

_SIGNAL_NAMES = (
    "stability_score",
    "coherence_score",
    "factual_hallucination_score",
    "semantic_instability_score",
    "semantic_risk",
    "confidence",
)


def observation_to_row(obs: Observation) -> dict[str, Any]:
    row: dict[str, Any] = {
        "id_campaign_id": obs.campaign_id,
        "id_dataset_id": obs.dataset_id,
        "id_prompt_id": obs.prompt_id,
        "id_prompt_text": obs.prompt,
        "id_prompt_family": obs.prompt_family,
        "id_domain": obs.domain,
        "id_provider": obs.provider,
        "id_model": obs.model,
        "id_arm_id": obs.arm_id,
        "id_repetition_index": obs.repetition_index,
        "id_planned_repetitions": obs.planned_repetitions,
        "id_timestamp_utc": obs.timestamp_utc,
    }

    m = obs.measurement
    row.update(
        {
            "nm_request_id": m.request_id if m else None,
            "nm_schema_version": m.schema_version if m else None,
            "nm_measurement_version": m.measurement_version if m else None,
            "nm_normalizer_version": m.normalizer_version if m else None,
            "nm_measurement_status": m.measurement_status if m else None,
            "nm_measurement_coverage": m.measurement_coverage if m else None,
            "nm_observation_class": m.observation_class if m else None,
            "nm_decision": m.decision if m else None,
        }
    )

    for name in _SIGNAL_NAMES:
        signal = m.signals.get(name) if m else None
        row[f"nm_{name}"] = signal.value if (signal and signal.is_usable()) else None
        row[f"nm_{name}_status"] = signal.status.value if signal else SignalStatus.NOT_MEASURED.value

    row["op_latency_ms"] = obs.latency_ms
    row["op_token_count"] = obs.token_count
    row["op_error"] = obs.error or ""

    return row


@dataclass
class CanonicalDataset:
    campaign_id: str
    rows: list[dict[str, Any]] = field(default_factory=list)

    @property
    def columns(self) -> tuple[str, ...]:
        return CANONICAL_COLUMNS

    @property
    def observation_count(self) -> int:
        return len(self.rows)

    @property
    def error_count(self) -> int:
        return sum(1 for row in self.rows if row.get("op_error"))

    def payload_hash(self) -> str:
        """Deterministic SHA-256 over the canonical rows (sorted keys, no
        whitespace), so the same observation set always hashes the same way,
        independent of collection order artifacts."""
        canonical_json = json.dumps(self.rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def build_canonical_dataset(campaign_id: str, observations: list[Observation]) -> CanonicalDataset:
    rows = [observation_to_row(obs) for obs in observations]
    # Deterministic ordering: prompt, then arm, then repetition.
    rows.sort(key=lambda r: (str(r["id_prompt_id"]), str(r["id_arm_id"]), int(r["id_repetition_index"])))
    return CanonicalDataset(campaign_id=campaign_id, rows=rows)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
