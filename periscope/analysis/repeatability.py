"""analyze_repeatability(): how consistent repeated calls are for the same
prompt run against the same arm -- the within-condition dispersion that
`repetitions > 1` in a campaign exists to measure.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from periscope.analysis._util import METRIC_LABELS, NM_METRIC_COLUMNS, group_rows, numeric_values, stats
from periscope.datasets.canonicalize import CanonicalDataset


@dataclass
class RepeatabilityCell:
    prompt_id: str
    arm_id: str
    metric: str
    repetitions_observed: int
    distribution: dict


@dataclass
class RepeatabilityReport:
    campaign_id: str
    cells: list[RepeatabilityCell] = field(default_factory=list)

    def least_repeatable(self, metric: str = "nm_stability_score", top: int = 10) -> list[RepeatabilityCell]:
        candidates = [c for c in self.cells if c.metric == metric and c.distribution["stdev"] is not None]
        return sorted(candidates, key=lambda c: -(c.distribution["stdev"] or 0))[:top]


def analyze_repeatability(dataset: CanonicalDataset) -> RepeatabilityReport:
    by_cell = group_rows(dataset.rows, lambda r: (r["id_prompt_id"], r["id_arm_id"]))

    cells = []
    for (prompt_id, arm_id), rows in by_cell.items():
        for column in NM_METRIC_COLUMNS:
            values = numeric_values(rows, column)
            cells.append(
                RepeatabilityCell(
                    prompt_id=prompt_id,
                    arm_id=arm_id,
                    metric=column,
                    repetitions_observed=len(rows),
                    distribution=stats(values),
                )
            )
    return RepeatabilityReport(campaign_id=dataset.campaign_id, cells=cells)
