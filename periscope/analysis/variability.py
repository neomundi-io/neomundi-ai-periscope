"""analyze_variability(): dispersion across the whole campaign, and which
prompts/arms carry the largest observed spread -- the "where should I look
first" signal for the Executive Snapshot.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from periscope.analysis._util import METRIC_LABELS, NM_METRIC_COLUMNS, OP_METRIC_COLUMNS, numeric_values, stats
from periscope.analysis.comparison import analyze_prompt_level_variation
from periscope.datasets.canonicalize import CanonicalDataset


@dataclass
class VariabilityReport:
    campaign_id: str
    metric_distributions: dict[str, dict] = field(default_factory=dict)
    most_variable_prompts: list[dict] = field(default_factory=list)


def analyze_variability(dataset: CanonicalDataset, spread_metric: str = "nm_stability_score", top: int = 5) -> VariabilityReport:
    distributions = {}
    for column in NM_METRIC_COLUMNS + OP_METRIC_COLUMNS:
        distributions[column] = stats(numeric_values(dataset.rows, column))

    most_variable = [
        r for r in analyze_prompt_level_variation(dataset, metric=spread_metric) if r["spread"] is not None
    ][:top]

    return VariabilityReport(
        campaign_id=dataset.campaign_id,
        metric_distributions=distributions,
        most_variable_prompts=most_variable,
    )
