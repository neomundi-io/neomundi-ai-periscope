"""build_baseline(): establish a reference level for a canonical dataset (or
one arm of it) -- distributions per metric, to be compared against later
campaigns or other arms.

This is Periscope-derived analysis. It never overwrites or recomputes a
NeoMundi signal; it only summarizes the NeoMundi signals and campaign
operational data already present in the canonical dataset.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from periscope.analysis._util import METRIC_LABELS, NM_METRIC_COLUMNS, OP_METRIC_COLUMNS, numeric_values, stats
from periscope.datasets.canonicalize import CanonicalDataset


@dataclass
class BaselineMetric:
    metric: str
    label: str
    origin: str  # "neomundi_measurement" | "campaign_operational"
    distribution: dict


@dataclass
class Baseline:
    campaign_id: str
    arm_id: str | None  # None => baseline computed across all arms in the dataset
    observation_count: int
    metrics: list[BaselineMetric] = field(default_factory=list)

    def metric(self, name: str) -> BaselineMetric | None:
        return next((m for m in self.metrics if m.metric == name), None)


def build_baseline(dataset: CanonicalDataset, arm_id: str | None = None) -> Baseline:
    rows = dataset.rows if arm_id is None else [r for r in dataset.rows if r["id_arm_id"] == arm_id]

    metrics = []
    for column in NM_METRIC_COLUMNS:
        metrics.append(
            BaselineMetric(
                metric=column,
                label=METRIC_LABELS[column],
                origin="neomundi_measurement",
                distribution=stats(numeric_values(rows, column)),
            )
        )
    for column in OP_METRIC_COLUMNS:
        metrics.append(
            BaselineMetric(
                metric=column,
                label=METRIC_LABELS[column],
                origin="campaign_operational",
                distribution=stats(numeric_values(rows, column)),
            )
        )

    return Baseline(
        campaign_id=dataset.campaign_id,
        arm_id=arm_id,
        observation_count=len(rows),
        metrics=metrics,
    )
