"""analyze_finops(): latency, tokens, and efficiency -- cost only when the
caller supplies a dated, versioned price table.

Mirrors the posture the Euria reporting generator already used as
methodological reference: `cost_score` (when a NeoMundi cost-related signal
is present) is summarized as a *signal*, and no monetary figure is invented
without an explicit external price table. This is a deliberate,
non-negotiable product rule -- see docs/METRIC_BOUNDARIES.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from periscope.analysis._util import group_rows, numeric_values, stats
from periscope.datasets.canonicalize import CanonicalDataset


@dataclass
class PriceTable:
    """An explicit, dated, versioned price table supplied by the caller.
    Periscope never fabricates one."""

    currency: str
    priced_at: str  # ISO date the prices were valid
    price_per_1k_input_tokens: dict[str, float] = field(default_factory=dict)   # keyed by model
    price_per_1k_output_tokens: dict[str, float] = field(default_factory=dict)  # keyed by model


@dataclass
class FinOpsReport:
    campaign_id: str
    latency_ms: dict
    token_count: dict
    by_arm_latency_ms: dict[str, dict] = field(default_factory=dict)
    by_arm_token_count: dict[str, dict] = field(default_factory=dict)
    estimated_cost: dict[str, float] | None = None  # arm_id -> total, only if a PriceTable was supplied
    price_table_used: PriceTable | None = None


def analyze_finops(dataset: CanonicalDataset, price_table: PriceTable | None = None) -> FinOpsReport:
    by_arm = group_rows(dataset.rows, lambda r: r["id_arm_id"])

    by_arm_latency = {arm: stats(numeric_values(rows, "op_latency_ms")) for arm, rows in by_arm.items()}
    by_arm_tokens = {arm: stats(numeric_values(rows, "op_token_count")) for arm, rows in by_arm.items()}

    estimated_cost = None
    if price_table is not None:
        estimated_cost = {}
        for row in dataset.rows:
            arm_id = row["id_arm_id"]
            model = row["id_model"]
            tokens = row.get("op_token_count")
            if tokens is None:
                continue
            # Total tokens are treated as output tokens absent a documented
            # input/output split in the canonical dataset -- a conservative,
            # explicitly-stated simplification, not a NeoMundi figure.
            price_per_1k = price_table.price_per_1k_output_tokens.get(model)
            if price_per_1k is None:
                continue
            estimated_cost[arm_id] = estimated_cost.get(arm_id, 0.0) + (tokens / 1000.0) * price_per_1k

    return FinOpsReport(
        campaign_id=dataset.campaign_id,
        latency_ms=stats(numeric_values(dataset.rows, "op_latency_ms")),
        token_count=stats(numeric_values(dataset.rows, "op_token_count")),
        by_arm_latency_ms=by_arm_latency,
        by_arm_token_count=by_arm_tokens,
        estimated_cost=estimated_cost,
        price_table_used=price_table,
    )
