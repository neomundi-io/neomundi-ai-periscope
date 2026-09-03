"""analyze_longitudinal_change(): compare a metric across an ordered series
of campaigns (e.g. the same corpus run weekly against the same arm).

Kept intentionally simple in the open engine -- the full longitudinal
drill-down (per-period event table, review-priority heuristic across
periods) is part of the advanced Longitudinal Report, documented but not
shipped as a public report generator in this build (see
docs/REPORT_LIBRARY.md).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from periscope.analysis._util import METRIC_LABELS, NM_METRIC_COLUMNS, OP_METRIC_COLUMNS, numeric_values, stats
from periscope.datasets.canonicalize import CanonicalDataset

ALL_METRIC_COLUMNS = NM_METRIC_COLUMNS + OP_METRIC_COLUMNS


@dataclass
class PeriodPoint:
    period_label: str
    campaign_id: str
    stats_by_metric: dict[str, dict]


@dataclass
class LongitudinalSeries:
    metric: str
    label: str
    points: list[PeriodPoint]
    deltas_vs_previous: list[float | None]


def analyze_longitudinal_change(periods: list[tuple[str, CanonicalDataset]]) -> list[LongitudinalSeries]:
    """`periods` must already be in chronological order -- this function does
    not infer chronology from campaign_id or file timestamps."""
    points_by_metric: dict[str, list[PeriodPoint]] = {m: [] for m in ALL_METRIC_COLUMNS}

    for period_label, dataset in periods:
        for column in ALL_METRIC_COLUMNS:
            points_by_metric[column].append(
                PeriodPoint(
                    period_label=period_label,
                    campaign_id=dataset.campaign_id,
                    stats_by_metric={column: stats(numeric_values(dataset.rows, column))},
                )
            )

    series = []
    for column in ALL_METRIC_COLUMNS:
        points = points_by_metric[column]
        means = [p.stats_by_metric[column]["mean"] for p in points]
        deltas: list[float | None] = [None]
        for prev, curr in zip(means, means[1:]):
            deltas.append(curr - prev if (prev is not None and curr is not None) else None)
        series.append(LongitudinalSeries(metric=column, label=METRIC_LABELS[column], points=points, deltas_vs_previous=deltas))

    return series
