# Reporting

Two public report generators ship in this build:
**Executive Snapshot** and **Model Release Benchmark Report**
(`periscope/reports/open/`). The full list of report types, including
advanced ones available on request, is in
[REPORT_LIBRARY.md](./REPORT_LIBRARY.md).

## Pipeline

```text
canonical dataset  ->  analysis (baseline/comparison/audit/finops/...)  ->  report
```

Reports never read raw campaign output directly and never recompute a
metric independently of `periscope/analysis/*` — see
[METRIC_BOUNDARIES.md](./METRIC_BOUNDARIES.md).

## Shared infrastructure (`periscope/reports/common/`)

- `html.py` — escaping, metric cards, tables, meta grids; no templating
  engine, small explicit functions.
- `charts.py` — dependency-free inline SVG bar charts and sparklines (no
  matplotlib/raster dependency, unlike the private methodological
  reference).
- `pdf.py` — HTML -> PDF via Playwright, falling back to WeasyPrint; if
  neither is installed, HTML generation still succeeds and PDF is skipped
  with a clear message.
- `localization.py` — structured FR/EN label dictionaries, per report.
  Unlike the private reference's "render once, machine-translate the
  rendered HTML" approach, both languages are first-class from the start.
- `rendering.py` — the shared header, campaign meta grid, and
  interpretation-boundary footer every report carries, from one
  implementation.

## Executive Snapshot

`periscope.reports.open.executive_snapshot.generate_executive_snapshot`

A short brief answering: what was tested, principal operational signals,
strongest variations (largest per-prompt stability spread across arms),
observations deserving further investigation (`run_audit` findings), and
limitations. See [docs/METRIC_BOUNDARIES.md](./METRIC_BOUNDARIES.md) for the
"measured signal, not verdict" boundary every section respects.

## Model Release Benchmark Report

`periscope.reports.open.model_release_benchmark.generate_model_release_benchmark`

For teams evaluating a new model release against a baseline, a previous
version, or peers. Covers protocol, dataset, models/providers tested, runs,
measurement versions, behavioural/stability/factual-risk/semantic/latency
comparisons, prompt-level differences, distribution summary, notable
changes, limits, and a reproducibility manifest with file hashes. See
[BENCHMARK.md](./BENCHMARK.md).

Explicitly **not a universal leaderboard** — see the "not a leaderboard"
notice rendered at the top of every instance of this report, and
[docs/CAMPAIGN_MODEL.md](./CAMPAIGN_MODEL.md) for how to set up a new-model
vs. baseline campaign.

## Generating reports

```bash
periscope report <campaign_id> --type snapshot --lang both
periscope report <campaign_id> --type model-release-benchmark --lang en --reference-arm "openai:gpt-4o-2024-11-20"
```

Both commands write HTML always, and PDF when a PDF engine is available
(`--no-pdf` to skip). See [QUICKSTART.md](../QUICKSTART.md) for the full
walkthrough.

## Simulated campaigns

A report generated from a campaign run with `--simulate` carries an
explicit synthetic-data notice at the top (from
`campaign_manifest.json`'s `simulated: true`) — it is never presented as if
it came from real NeoMundi measurements.
