"""compare_runs / compare_models / compare_providers: delta between two or
more groups of observations within the same canonical dataset (or across two
canonical datasets sharing the same dataset_id).

Every comparison reports a measured delta, never a ranking verdict. Reading
"Model X is best" into a ComparisonTable is a downstream interpretation, not
something this module states.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from periscope.analysis._util import METRIC_LABELS, NM_METRIC_COLUMNS, OP_METRIC_COLUMNS, group_rows, numeric_values, stats
from periscope.datasets.canonicalize import CanonicalDataset

ALL_METRIC_COLUMNS = NM_METRIC_COLUMNS + OP_METRIC_COLUMNS


@dataclass
class MetricComparison:
    metric: str
    label: str
    group_stats: dict[str, dict]  # group_key -> stats()
    deltas: dict[str, float | None]  # "groupB_vs_groupA" -> mean(B) - mean(A), only for pairs vs the reference group


@dataclass
class ComparisonTable:
    dimension: str  # "arm" | "provider" | "model" | "run" (campaign_id)
    reference_group: str | None
    groups: list[str]
    observation_counts: dict[str, int]
    metrics: list[MetricComparison] = field(default_factory=list)


def _compare_by(rows: list[dict], group_key_fn, dimension: str, reference_group: str | None) -> ComparisonTable:
    groups = group_rows(rows, group_key_fn)
    group_names = sorted(str(g) for g in groups)
    reference = reference_group if reference_group in group_names else (group_names[0] if group_names else None)

    metrics = []
    for column in ALL_METRIC_COLUMNS:
        group_stats = {name: stats(numeric_values(groups[name], column)) for name in group_names}
        deltas: dict[str, float | None] = {}
        ref_mean = group_stats.get(reference, {}).get("mean") if reference else None
        for name in group_names:
            if name == reference:
                continue
            other_mean = group_stats[name]["mean"]
            deltas[f"{name}_vs_{reference}"] = (
                other_mean - ref_mean if (other_mean is not None and ref_mean is not None) else None
            )
        metrics.append(
            MetricComparison(metric=column, label=METRIC_LABELS[column], group_stats=group_stats, deltas=deltas)
        )

    return ComparisonTable(
        dimension=dimension,
        reference_group=reference,
        groups=group_names,
        observation_counts={name: len(groups[name]) for name in group_names},
        metrics=metrics,
    )


def compare_runs(datasets: list[CanonicalDataset], reference_campaign_id: str | None = None) -> ComparisonTable:
    """Compare two or more canonical datasets (e.g. two campaigns run over
    time on the same corpus) as distinct groups."""
    rows: list[dict] = []
    for dataset in datasets:
        for row in dataset.rows:
            row = dict(row)
            row["_run_group"] = dataset.campaign_id
            rows.append(row)
    return _compare_by(rows, lambda r: r["_run_group"], dimension="run", reference_group=reference_campaign_id)


def compare_models(dataset: CanonicalDataset, reference_model: str | None = None) -> ComparisonTable:
    return _compare_by(dataset.rows, lambda r: r["id_model"], dimension="model", reference_group=reference_model)


def compare_providers(dataset: CanonicalDataset, reference_provider: str | None = None) -> ComparisonTable:
    return _compare_by(dataset.rows, lambda r: r["id_provider"], dimension="provider", reference_group=reference_provider)


def compare_arms(dataset: CanonicalDataset, reference_arm_id: str | None = None) -> ComparisonTable:
    return _compare_by(dataset.rows, lambda r: r["id_arm_id"], dimension="arm", reference_group=reference_arm_id)


def analyze_prompt_level_variation(dataset: CanonicalDataset, metric: str = "nm_stability_score") -> list[dict]:
    """Per-prompt delta for `metric` between arms, when the dataset contains
    more than one arm. Returns rows sorted by largest absolute spread first
    -- the basis for "most variable prompts" in the open reports."""
    by_prompt = group_rows(dataset.rows, lambda r: r["id_prompt_id"])
    records = []
    for prompt_id, prompt_rows in by_prompt.items():
        by_arm = group_rows(prompt_rows, lambda r: r["id_arm_id"])
        arm_means = {arm: stats(numeric_values(rows, metric))["mean"] for arm, rows in by_arm.items()}
        usable = {arm: v for arm, v in arm_means.items() if v is not None}
        spread = (max(usable.values()) - min(usable.values())) if len(usable) >= 2 else None
        records.append(
            {
                "prompt_id": prompt_id,
                "prompt_text": prompt_rows[0].get("id_prompt_text", ""),
                "arm_means": arm_means,
                "spread": spread,
            }
        )
    records.sort(key=lambda r: (r["spread"] is None, -(r["spread"] or 0)))
    return records
