"""build_benchmark(): the analysis backbone of the Model Release Benchmark
report -- new model vs baseline, model A vs model B, or N models/providers
at once, all from one canonical dataset.

Composes the other analysis modules rather than recomputing anything: this
is a Periscope-derived view, not a new measurement.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from periscope.analysis.baseline import Baseline, build_baseline
from periscope.analysis.comparison import ComparisonTable, analyze_prompt_level_variation, compare_arms
from periscope.analysis.repeatability import RepeatabilityReport, analyze_repeatability
from periscope.datasets.canonicalize import CanonicalDataset

NOT_A_LEADERBOARD_NOTICE = (
    "This is not a universal leaderboard. Results describe measured values "
    "on this corpus, protocol and measurement version only -- they do not "
    "establish that one model is 'better' outside this scope."
)


@dataclass
class BenchmarkResult:
    campaign_id: str
    reference_arm_id: str | None
    arms: list[str]
    baselines_by_arm: dict[str, Baseline] = field(default_factory=dict)
    arm_comparison: ComparisonTable | None = None
    repeatability: RepeatabilityReport | None = None
    prompt_level_variation: list[dict] = field(default_factory=list)
    notice: str = NOT_A_LEADERBOARD_NOTICE


def build_benchmark(dataset: CanonicalDataset, reference_arm_id: str | None = None) -> BenchmarkResult:
    arms = sorted({row["id_arm_id"] for row in dataset.rows})
    if reference_arm_id is None and arms:
        reference_arm_id = arms[0]

    baselines_by_arm = {arm_id: build_baseline(dataset, arm_id=arm_id) for arm_id in arms}

    return BenchmarkResult(
        campaign_id=dataset.campaign_id,
        reference_arm_id=reference_arm_id,
        arms=arms,
        baselines_by_arm=baselines_by_arm,
        arm_comparison=compare_arms(dataset, reference_arm_id=reference_arm_id) if len(arms) >= 2 else None,
        repeatability=analyze_repeatability(dataset),
        prompt_level_variation=analyze_prompt_level_variation(dataset) if len(arms) >= 2 else [],
    )
