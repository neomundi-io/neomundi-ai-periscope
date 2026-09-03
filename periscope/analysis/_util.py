"""Shared statistics helpers for the analysis library.

Internal module (leading underscore): every public analysis function lives
in benchmark.py / baseline.py / audit.py / evaluation.py / repeatability.py /
variability.py / longitudinal.py / comparison.py / finops.py, which import
from here rather than duplicating aggregation code five times.

Everything here operates on canonical dataset rows (see
datasets/canonicalize.py) and produces Periscope-derived analysis --
never written back into a canonical dataset, always returned as a separate
structure by the caller.
"""

from __future__ import annotations

import math
import statistics
from typing import Any, Callable, Iterable


def safe_float(value: Any) -> float | None:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def numeric_values(rows: list[dict], column: str) -> list[float]:
    out = []
    for row in rows:
        value = safe_float(row.get(column))
        if value is not None:
            out.append(value)
    return out


def _percentile(sorted_values: list[float], fraction: float) -> float:
    if len(sorted_values) == 1:
        return sorted_values[0]
    k = (len(sorted_values) - 1) * fraction
    lower = math.floor(k)
    upper = math.ceil(k)
    if lower == upper:
        return sorted_values[int(k)]
    return sorted_values[lower] + (sorted_values[upper] - sorted_values[lower]) * (k - lower)


def stats(values: list[float]) -> dict[str, float | int | None]:
    """count/mean/median/stdev/min/p05/p25/p75/p95/max over a list of floats.

    Returns None for every field when `values` is empty rather than raising
    -- a metric with zero usable observations is a legitimate outcome
    (e.g. a signal that was never measured across the whole campaign) and
    must be represented as "no data", not as a crash or as 0.
    """
    if not values:
        return {k: None for k in ("count", "mean", "median", "stdev", "min", "p05", "p25", "p75", "p95", "max")}
    ordered = sorted(values)
    return {
        "count": len(values),
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "stdev": statistics.pstdev(values) if len(values) > 1 else 0.0,
        "min": ordered[0],
        "p05": _percentile(ordered, 0.05),
        "p25": _percentile(ordered, 0.25),
        "p75": _percentile(ordered, 0.75),
        "p95": _percentile(ordered, 0.95),
        "max": ordered[-1],
    }


def group_rows(rows: list[dict], key_fn: Callable[[dict], Any]) -> dict[Any, list[dict]]:
    groups: dict[Any, list[dict]] = {}
    for row in rows:
        groups.setdefault(key_fn(row), []).append(row)
    return groups


def mean(values: Iterable[float]) -> float | None:
    values = list(values)
    return statistics.fmean(values) if values else None


NM_METRIC_COLUMNS = (
    "nm_stability_score",
    "nm_coherence_score",
    "nm_factual_hallucination_score",
    "nm_semantic_instability_score",
    "nm_semantic_risk",
    "nm_confidence",
)

OP_METRIC_COLUMNS = (
    "op_latency_ms",
    "op_token_count",
)

METRIC_LABELS = {
    "nm_stability_score": "Stability",
    "nm_coherence_score": "Coherence",
    "nm_factual_hallucination_score": "Factual-risk signal",
    "nm_semantic_instability_score": "Semantic instability",
    "nm_semantic_risk": "Semantic risk",
    "nm_confidence": "Confidence",
    "op_latency_ms": "Latency (ms)",
    "op_token_count": "Tokens",
}
