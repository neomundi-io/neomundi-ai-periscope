# NeoMundi AI Periscope Layer

[🇫🇷 Version française](./README_FR.md)

**Probe, benchmark, baseline and evaluate AI systems across models, providers and datasets.**

Run reproducible AI evaluation campaigns using NeoMundi runtime measurements, then turn the resulting observations into comparable datasets, analyses and decision-ready reports.

**One campaign engine · Multiple providers · Reproducible measurements · Comparable results · Decision-ready evidence**

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
Canonical Datasets  ->  Analysis  ->  Report Library
```

AI Periscope consumes NeoMundi measurements — it does not redefine them. See
[`docs/METRIC_BOUNDARIES.md`](./docs/METRIC_BOUNDARIES.md).

---

## Benchmark a new AI model when it ships

Run the same corpus against a newly released model and your current baseline.

AI Periscope captures NeoMundi runtime measurements, builds a comparable campaign dataset and produces a reproducible benchmark report.

```bash
periscope run my_campaign.yaml
periscope report my_campaign_id --type model-release-benchmark --lang en
```

Use cases:

- model release evaluation
- provider comparison
- migration assessment
- model version change
- pre-production baseline
- post-upgrade comparison

This is **not a universal leaderboard**. The report states measured deltas
under a documented corpus, protocol and measurement version — never "Model X
is the best model." See [`docs/BENCHMARK.md`](./docs/BENCHMARK.md).

---

## Two open reports, ready today

| Report | Answers | Command |
|---|---|---|
| **Executive Snapshot** | What was tested, what changed, what deserves attention | `periscope report <id> --type snapshot` |
| **Model Release Benchmark** | How does a new/other model compare on this corpus | `periscope report <id> --type model-release-benchmark` |

Both: HTML + PDF, FR + EN, built from a canonical dataset so results are
reproducible by a third party. See [`docs/REPORTING.md`](./docs/REPORTING.md).

### Advanced reporting — available on request

Full Metrology · Governance / Review · FinOps · Longitudinal · Compliance
Evidence · Custom.

The underlying analysis functions are already public in
[`periscope/analysis/`](./periscope/analysis/) — only the packaged report
rendering for these types is not shipped in this build. See
[`docs/REPORT_LIBRARY.md`](./docs/REPORT_LIBRARY.md) for what each one
covers.

**Contact NeoMundi through [neomundi.io](https://neomundi.io).**

---

## Quickstart

```bash
python -m pip install -e .

# No API keys needed:
periscope run examples/campaigns/sample_campaign.yaml --simulate
periscope report sample_release_check --type snapshot --lang both
```

Full walkthrough, including running against live NeoMundi + provider APIs:
[`QUICKSTART.md`](./QUICKSTART.md).

## What was tested must stay reproducible

Every campaign produces:

- a **canonical dataset** (`campaign_results.json` / `.csv`) — one row per
  observation, NeoMundi measurement fields (`nm_*`) and campaign operational
  fields (`op_*`) kept strictly separate from any Periscope-derived analysis;
- a **campaign manifest** (`campaign_manifest.json`) — dataset hash, arms,
  repetitions, measurement schema/engine versions observed, error count, and
  output file hashes.

Nothing is hidden: execution errors are counted and traceable, never
silently dropped. See [`docs/CAMPAIGN_MODEL.md`](./docs/CAMPAIGN_MODEL.md).

## Providers

Only providers NeoMundi documents are supported — none hardcoded beyond that
list (`periscope/providers/registry.py`):

```text
openai · anthropic · google (alias gemini) · mistral · cohere · deepseek
xai (alias grok) · perplexity · together · qwen · apertus · euria
```

## CLI

```text
periscope run campaign.yaml [--simulate]
periscope report <campaign_id> --type snapshot [--lang fr|en|both]
periscope report <campaign_id> --type model-release-benchmark [--reference-arm ARM]
```

## Documentation map

| Document | Purpose |
|---|---|
| [`QUICKSTART.md`](./QUICKSTART.md) | Get a first campaign and report in minutes |
| [`docs/PRODUCT_ARCHITECTURE.md`](./docs/PRODUCT_ARCHITECTURE.md) | How the engine, analysis library and report library fit together |
| [`docs/CAMPAIGN_MODEL.md`](./docs/CAMPAIGN_MODEL.md) | The `campaign.yaml` schema, execution plan, providers |
| [`docs/BENCHMARK.md`](./docs/BENCHMARK.md) · [`BASELINE.md`](./docs/BASELINE.md) · [`AUDIT.md`](./docs/AUDIT.md) · [`EVALUATION.md`](./docs/EVALUATION.md) | The analysis library |
| [`docs/REPORTING.md`](./docs/REPORTING.md) | The two open reports |
| [`docs/REPORT_LIBRARY.md`](./docs/REPORT_LIBRARY.md) | Full report catalogue, open + on request |
| [`docs/METRIC_BOUNDARIES.md`](./docs/METRIC_BOUNDARIES.md) | NeoMundi measurement vs. Periscope analysis — the rule everything else follows |
| [`VERSIONING.md`](./VERSIONING.md) | Package version vs. NeoMundi measurement versions |
| [`reference/NOTES.md`](./reference/NOTES.md) | Pointers to the normative NeoMundi sources this product aligns with |

## What this product does not claim

AI Periscope does not certify, does not declare a system safe or unsafe,
compliant or non-compliant, and does not produce a universal ranking of
models. It measures, via NeoMundi, and turns those measurements into
comparable, reproducible evidence — the interpretation, policy and decision
remain the consuming organization's. See
[`docs/METRIC_BOUNDARIES.md`](./docs/METRIC_BOUNDARIES.md).

## Private methodological reference

The analysis library and open reports were generalized from NeoMundi's
private Euria/Fatima reporting generator, used here as a methodological
reference only. That generator, its client-specific report logic, and any
client-identifying dataset are **not** part of this repository.

## License

[MIT](./LICENSE) — Copyright (c) 2026 NeoMundi.io
