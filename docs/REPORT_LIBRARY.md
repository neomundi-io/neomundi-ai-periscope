# Report Library

AI Periscope is the campaign / benchmark / baseline / evaluation engine.
Around it, NeoMundi maintains a Report Library: a growing set of report
types built from the same canonical datasets and the same analysis library
(`periscope/analysis/`), so every report — public or advanced — reads the
same numbers the same way (see [METRIC_BOUNDARIES.md](./METRIC_BOUNDARIES.md)).

Two report types are public and fully implemented in this build. The rest
are documented here and available on request.

| Report | Purpose | Availability |
|---|---|---|
| Executive Snapshot | Fast decision brief: what was tested, what changed, what deserves attention | **Open** |
| Model Release Benchmark | Compare a new model against a baseline or peers | **Open** |
| Full Metrology Report | Deep distributions, repeatability, longitudinal analysis | On request |
| Governance / Review Report | Review prioritization and decision-support objects | On request |
| FinOps Report | Tokens, latency, efficiency and cost-oriented analysis | On request |
| Longitudinal Report | Compare campaigns over time | On request |
| Compliance Evidence Report | Map campaign evidence to external compliance workflows | On request |
| Custom Report | Client-specific analysis and reporting | Contact NeoMundi |

## Open reports

- **Executive Snapshot** — `periscope report <campaign> --type snapshot`.
  See [REPORTING.md](./REPORTING.md).
- **Model Release Benchmark Report** — `periscope report <campaign> --type
  model-release-benchmark`. See [BENCHMARK.md](./BENCHMARK.md).

## Advanced reports (on request)

These are documented, and their underlying analysis functions are already
public in `periscope/analysis/`, but their full report *rendering* (cover
pages, multi-section HTML/PDF layout) is not shipped as a public generator
in this build — see [`periscope/reports/advanced/README.md`](../periscope/reports/advanced/README.md)
for why, and for how to build on the analysis library directly today.

- **Full Metrology Report** — complete distributions (count, mean, median,
  stdev, percentiles) per metric and per arm, repeatability across
  repetitions, and longitudinal series when multiple campaigns are
  available. Backed by `analysis.baseline`, `analysis.repeatability`,
  `analysis.longitudinal`.
- **Governance / Review Report** — a full review-priority map, an
  interpretation grammar, and a documented (non-normative) action-rule
  table. Backed by `analysis.audit`. See [AUDIT.md](./AUDIT.md) for why this
  heuristic is explicitly not a NeoMundi signal.
- **FinOps Report** — latency/token efficiency trends and, only when a
  dated, versioned price table is supplied, an estimated cost breakdown.
  Backed by `analysis.finops`. Never invents a monetary figure without an
  explicit price table.
- **Longitudinal Report** — a full period-over-period drill-down (an
  extended version of the Executive Snapshot's "strongest variations,"
  across more than two periods). Backed by `analysis.longitudinal`.
- **Compliance Evidence Report** — maps campaign evidence (manifest,
  canonical dataset, analysis outputs) onto an external compliance
  framework's evidence requirements. Necessarily specific to the framework
  in question; built on request.
- **Custom Report** — anything else built directly on
  `periscope/analysis/*` and `periscope/reports/common/` for a specific
  client need.

## Availability

Advanced and custom reporting packages are available on request.
**Contact NeoMundi through neomundi.io.**
