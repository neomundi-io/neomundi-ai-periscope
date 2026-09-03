# Product Architecture

```text
NeoMundi Runtime Measurement Layer
        |
        v
NeoMundi AI Periscope Layer
        |
        v
Campaign / Benchmark / Baseline / Evaluation
        |
        v
Canonical Datasets
        |
        v
Analysis
        |
        v
Report Library
```

AI Periscope is a campaign, benchmark, baseline, audit and evaluation layer
built **on top of** the NeoMundi Runtime Measurement Layer. It consumes
NeoMundi measurements; it does not redefine them (see
[METRIC_BOUNDARIES.md](./METRIC_BOUNDARIES.md)).

## One engine, many views

```text
run_campaign()  ->  Canonical Dataset
                          |
        +-----------------+-----------------+
        |         |          |              |
   build_baseline  compare_*  run_audit  analyze_finops  ...
        |         |          |              |
        +-----------------+-----------------+
                          |
                    Report Library
```

`run_campaign()` is the only thing that talks to NeoMundi / providers and
produces a canonical dataset. Every other capability — benchmark, baseline,
audit, evaluation, repeatability, variability, longitudinal, FinOps, and
every report — is a *function computed from* that canonical dataset. None of
them re-run the campaign or recompute a NeoMundi measurement differently.

## Package layout

```text
periscope/
    campaign/       configuration.py, repetition.py, runner.py
    providers/       registry.py, adapter.py
    datasets/        loader.py, validation.py, canonicalize.py
    measurement/     client.py, simulated.py, runtime.py, contracts.py
    analysis/        benchmark.py, baseline.py, audit.py, evaluation.py,
                      repeatability.py, variability.py, longitudinal.py,
                      comparison.py, finops.py
    reports/
        open/        executive_snapshot.py, model_release_benchmark.py
        advanced/     README.md (documented, available on request)
        common/       rendering.py, charts.py, html.py, pdf.py, localization.py
    export/          json_export.py, csv_export.py, manifest.py
    cli.py
```

- **campaign/** — what a campaign is (`CampaignConfig`), how it expands into
  an execution plan (1 dataset x N provider/model arms x N repetitions,
  without duplicating the engine — see
  [CAMPAIGN_MODEL.md](./CAMPAIGN_MODEL.md)), and the orchestration loop.
- **providers/** — a registry of the providers NeoMundi documents
  (`API_INTEGRATION_GUIDE.md` section 3.1), and a thin adapter to the
  `/v1/govern/stream` payload shape. No provider-specific logic in the core
  engine.
- **datasets/** — loading a CSV/JSON prompt corpus, validating it, and
  turning campaign observations into the canonical dataset.
- **measurement/** — the real NeoMundi API client (3-step flow), a
  deterministic offline simulator for tests and demos, wire-format
  normalization, and the field vocabulary/rules from
  [METRIC_BOUNDARIES.md](./METRIC_BOUNDARIES.md).
- **analysis/** — the derived-analysis library (see below).
- **reports/open/** — the two public report generators (see
  [REPORTING.md](./REPORTING.md)).
- **reports/advanced/** — documentation only; see
  [REPORT_LIBRARY.md](./REPORT_LIBRARY.md).
- **export/** — canonical dataset JSON/CSV writers and the campaign
  manifest (hashes, versions, reproducibility record).

## Analysis library

| Function | Module | Purpose |
|---|---|---|
| `build_baseline` | `analysis.baseline` | Reference distributions for a dataset or one arm — see [BASELINE.md](./BASELINE.md) |
| `compare_runs` / `compare_models` / `compare_providers` / `compare_arms` | `analysis.comparison` | Measured deltas between groups — see [BENCHMARK.md](./BENCHMARK.md) |
| `analyze_prompt_level_variation` | `analysis.comparison` | Per-prompt spread across arms |
| `analyze_repeatability` | `analysis.repeatability` | Within-condition dispersion across repetitions |
| `analyze_variability` | `analysis.variability` | Dataset-wide dispersion + most variable prompts |
| `analyze_longitudinal_change` | `analysis.longitudinal` | Metric change across an ordered series of campaigns |
| `analyze_finops` | `analysis.finops` | Latency/token efficiency, cost only with an explicit price table |
| `run_audit` | `analysis.audit` | Review-priority heuristic — see [AUDIT.md](./AUDIT.md) |
| `run_evaluation` | `analysis.evaluation` | Corpus/protocol/anomalies/limitations summary — see [EVALUATION.md](./EVALUATION.md) |
| `build_benchmark` | `analysis.benchmark` | Composes the above for the Model Release Benchmark report |

## What this build ships vs. documents

Two report generators are public and fully implemented:
**Executive Snapshot** and **Model Release Benchmark Report**
(`periscope/reports/open/`). The full analysis library above is public and
usable directly. Additional report *renderers* (Full Metrology, Governance /
Review, FinOps, Longitudinal, Compliance Evidence, Custom) are documented in
[REPORT_LIBRARY.md](./REPORT_LIBRARY.md) as available on request, not shipped
as public generators in this build.
