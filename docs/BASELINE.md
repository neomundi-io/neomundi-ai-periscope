# Baseline

`periscope.analysis.baseline.build_baseline(dataset, arm_id=None)` computes a
reference distribution for every NeoMundi measurement field and every
campaign operational field (see [METRIC_BOUNDARIES.md](./METRIC_BOUNDARIES.md)),
either across the whole canonical dataset or for one arm.

```python
from periscope.analysis.baseline import build_baseline

overall = build_baseline(canonical)                       # all arms
per_arm = build_baseline(canonical, arm_id="openai:gpt-4o-2024-11-20")
```

Each `BaselineMetric` carries:

- `metric` — the canonical column name (`nm_stability_score`, `op_latency_ms`, ...)
- `origin` — `"neomundi_measurement"` or `"campaign_operational"`, never blended
- `distribution` — `count, mean, median, stdev, min, p05, p25, p75, p95, max`
  (all `None` if the metric was never usably measured — see
  `periscope.analysis._util.stats`)

A baseline is descriptive, not evaluative: it establishes "what does this
arm's distribution currently look like," to be compared against later
campaigns (`compare_runs`) or other arms (`compare_arms` /
`compare_models` / `compare_providers`) — see
[BENCHMARK.md](./BENCHMARK.md).

Used by the **Executive Snapshot** (aggregate distributions) and the
**Model Release Benchmark Report** (per-arm distribution summary, section
14) — see [REPORTING.md](./REPORTING.md).
