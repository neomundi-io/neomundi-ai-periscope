"""Turns raw NeoMundi API payloads into a normalized MeasurementRecord.

This is the only place in Periscope that reads NeoMundi's wire format
(field-shape variants documented in API_INTEGRATION_GUIDE.md). Everything
downstream (canonicalization, analysis, reports) works against
`MeasurementRecord` / `ObservedSignal`, not raw dicts.
"""

from __future__ import annotations

from typing import Any

from periscope.measurement.contracts import (
    MeasurementRecord,
    ObservedSignal,
    SignalStatus,
    NEOMUNDI_SIGNAL_FIELDS,
)


def _dig(obj: Any, path: str) -> Any:
    """Resolve a dotted path like 'quality.stability_score' against a dict."""
    node = obj
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def _first(obj: dict, paths: list[str]) -> Any:
    for path in paths:
        value = _dig(obj, path)
        if value not in (None, ""):
            return value
    return None


# Accepted field-shape variants for the /v1/govern response, in priority
# order (first match wins) -- per API_INTEGRATION_GUIDE.md section 4.
GOVERN_RESPONSE_PATHS: dict[str, list[str]] = {
    "request_id": ["request_id"],
    "schema_version": ["identity.schema_version", "schema_version"],
    "measurement_version": ["provenance.measurement_version", "measurement_version"],
    "normalizer_version": ["provenance.normalizer_version", "normalizer_version"],
    "measurement_status": ["observation.measurement_status", "measurement_status"],
    "measurement_coverage": ["observation.measurement_coverage", "measurement_coverage"],
    "observation_class": [
        "observation.observed_signals.observation_class",
        "observation_class",
    ],
    "decision": ["governance.decision", "decision"],
    "stability_score": [
        "observation.observed_signals.stability_score",
        "quality.stability_score",
        "stability_score",
    ],
    "coherence_score": [
        "observation.observed_signals.coherence_score",
        "coherence_score",
    ],
    "factual_hallucination_score": [
        "observation.observed_signals.factual_hallucination_score",
        "factual_hallucination_score",
    ],
    "semantic_instability_score": [
        "observation.observed_signals.semantic_instability_score",
        "semantic_instability_score",
    ],
    "semantic_risk": [
        "observation.observed_signals.semantic_risk",
        "semantic_risk",
    ],
    "confidence": [
        "observation.observed_signals.confidence",
        "confidence",
    ],
}

# Chunk/response text and operational fields exposed by /v1/govern/stream.
STREAM_RESPONSE_TEXT_PATHS = ["response_text", "llm_response", "output_text", "response", "provider_response.text"]
STREAM_CHUNK_TEXT_PATHS = ["content", "delta.content", "text", "chunk"]
STREAM_TOKEN_COUNT_PATHS = [
    "token_count",
    "total_tokens",
    "tokens_so_far",
    "usage.total_tokens",
    "usage.output_tokens",
    "provider_usage.total_tokens",
    "provider_usage.output_tokens",
]
STREAM_LATENCY_PATHS = ["latency_ms", "processing_time_ms"]
STREAM_REQUEST_ID_PATHS = ["request_id"]


def extract_stream_chunk_text(event: dict) -> str | None:
    value = _first(event, STREAM_CHUNK_TEXT_PATHS)
    return value if isinstance(value, str) else None


def extract_stream_final_text(events: list[dict]) -> str | None:
    for event in reversed(events):
        value = _first(event, STREAM_RESPONSE_TEXT_PATHS)
        if isinstance(value, str) and value:
            return value
    return None


def extract_stream_token_count(events: list[dict]) -> int | None:
    for event in reversed(events):
        value = _first(event, STREAM_TOKEN_COUNT_PATHS)
        if value is not None:
            try:
                return int(value)
            except (TypeError, ValueError):
                continue
    return None


def extract_stream_latency_ms(events: list[dict]) -> float | None:
    for event in reversed(events):
        value = _first(event, STREAM_LATENCY_PATHS)
        if value is not None:
            try:
                return float(value)
            except (TypeError, ValueError):
                continue
    return None


def extract_stream_request_id(events: list[dict]) -> str | None:
    """The *stream* request_id -- distinct from the measurement request_id.

    Kept only for traceability of step 1; never used to fetch the RGC
    contract in step 3 (see API_INTEGRATION_GUIDE.md section 3, warning box).
    """
    for event in events:
        value = _first(event, STREAM_REQUEST_ID_PATHS)
        if value:
            return str(value)
    return None


def _signal_status_map(raw: dict) -> dict[str, str]:
    """RGC v0.2 per-signal status map, if present."""
    status_map = _dig(raw, "observation.observed_signals.signal_status")
    return status_map if isinstance(status_map, dict) else {}


def build_measurement_record(raw_govern_response: dict) -> MeasurementRecord:
    """Normalize a /v1/govern response (v0.1 or v0.2 shaped) into a MeasurementRecord.

    Never invents a value for a missing signal. Under v0.2, a signal's
    declared `signal_status` is respected even if a numeric value happens to
    be present in the payload -- status governs usability, not presence.
    """

    status_map = _signal_status_map(raw_govern_response)

    signals: dict[str, ObservedSignal] = {}
    for name in NEOMUNDI_SIGNAL_FIELDS:
        if name in ("observation_class", "decision"):
            continue  # categorical, not a numeric signal
        paths = GOVERN_RESPONSE_PATHS.get(name, [name])
        raw_value = _first(raw_govern_response, paths)

        declared_status = status_map.get(name)
        if declared_status is not None:
            try:
                status = SignalStatus(declared_status)
            except ValueError:
                status = SignalStatus.NOT_MEASURED
        else:
            # v0.1 has no explicit status: infer from presence.
            status = SignalStatus.MEASURED if raw_value is not None else SignalStatus.NOT_MEASURED

        value: float | None
        if status == SignalStatus.MEASURED and raw_value is not None:
            try:
                value = float(raw_value)
            except (TypeError, ValueError):
                value = None
                status = SignalStatus.NOT_MEASURED
        else:
            value = None

        signals[name] = ObservedSignal(name=name, value=value, status=status)

    coverage_raw = _first(raw_govern_response, GOVERN_RESPONSE_PATHS["measurement_coverage"])
    coverage = None
    if coverage_raw is not None:
        try:
            coverage = float(coverage_raw)
        except (TypeError, ValueError):
            coverage = None

    return MeasurementRecord(
        request_id=_first(raw_govern_response, GOVERN_RESPONSE_PATHS["request_id"]),
        schema_version=_first(raw_govern_response, GOVERN_RESPONSE_PATHS["schema_version"]),
        measurement_version=_first(raw_govern_response, GOVERN_RESPONSE_PATHS["measurement_version"]),
        normalizer_version=_first(raw_govern_response, GOVERN_RESPONSE_PATHS["normalizer_version"]),
        measurement_status=_first(raw_govern_response, GOVERN_RESPONSE_PATHS["measurement_status"]),
        measurement_coverage=coverage,
        observation_class=_first(raw_govern_response, GOVERN_RESPONSE_PATHS["observation_class"]),
        decision=_first(raw_govern_response, GOVERN_RESPONSE_PATHS["decision"]),
        signals=signals,
        raw=raw_govern_response,
    )
