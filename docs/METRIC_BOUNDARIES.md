# Metric Boundaries

AI Periscope keeps three kinds of data strictly separate, on every canonical
dataset row, in every analysis output, and in every report. This document is
the single source of truth for that separation — every other doc and every
report links back here rather than restating it.

```text
NeoMundi measurement   !=   campaign operational data   !=   Periscope-derived analysis
```

## 1. NeoMundi measurement (`nm_*` columns)

Signals returned by the NeoMundi Runtime Measurement Layer's `/v1/govern`
response: `stability_score`, `coherence_score`, `factual_hallucination_score`,
`semantic_instability_score`, `semantic_risk`, `confidence`,
`observation_class`, `decision` (`ALLOW`/`FLAG`/`REROUTE`/`HUMAN_REVIEW`/`STOP`),
plus their measurement metadata (`schema_version`, `measurement_version`,
`normalizer_version`, `measurement_status`, `measurement_coverage`).

Periscope **never recomputes these differently** and never overwrites a
missing value with a default. A signal that was not measured (RGC v0.2
`signal_status = not_measured` or `insufficient_coverage`, or simply absent
under RGC v0.1) is stored as `null` / `None`, and every per-signal status is
preserved alongside its value (`nm_<signal>_status`). See
`periscope/measurement/contracts.py` and `periscope/measurement/runtime.py`.

**A NeoMundi signal is a measurement, not a verdict.** `high stability !=
factual correctness`, `FLAG != proven error`, `ALLOW != proven truth`,
`within_bounds != globally safe`. This mirrors the NeoMundi Runtime
Measurement Layer's own `docs/CONSUMER_BOUNDARIES.md`.

## 2. Campaign operational data (`op_*` columns)

`latency_ms` and `token_count` are captured by the Periscope client itself
while running the campaign (timing the call, counting tokens in the
reconstructed response), then submitted to NeoMundi as `raw_metrics` context
for the `/v1/govern` call. They travel alongside the measurement record, but
they are **not a NeoMundi-computed signal** — they are Periscope's own
runtime/operational observation of the call. This is why they get their own
`op_` namespace rather than being folded into `nm_`.

## 3. Periscope-derived analysis

Everything produced by `periscope/analysis/*` — baselines, comparisons,
repeatability, variability, longitudinal series, audit/review priority,
FinOps summaries, benchmark tables. This is Periscope's own computation on
top of (1) and (2).

**Derived analysis is never written back into a canonical dataset row.** It
always lives in a separate structure (a `Baseline`, a `ComparisonTable`, an
`AuditReport`, ...), so a canonical dataset on disk can never be mistaken for
an analysis result, and a report can never accidentally present a derived
number as if NeoMundi had measured it. `tests/test_no_metric_confusion.py`
enforces this mechanically.

### Review-priority heuristic (`HIGH_REVIEW` / `REVIEW` / `ROUTINE`)

`periscope/analysis/audit.py` classifies arms/prompts into a descriptive
review-priority level, carried over as a starting point from NeoMundi's
private Euria/Fatima methodological reference. It is:

- **not a NeoMundi signal** — NeoMundi does not emit a review-priority field;
- **not an official NeoMundi threshold** — NeoMundi publishes no official
  numeric thresholds for its signals (`docs/CONSUMER_BOUNDARIES.md`, "No
  inferred thresholds"); the defaults in `AuditThresholds` are a Periscope
  configuration choice, not a NeoMundi norm, and should be tuned per
  campaign;
- **not an automated decision** — it prioritizes attention, it does not
  ALLOW, BLOCK, or otherwise act.

Every `AuditFinding` carries `NO_OFFICIAL_THRESHOLDS_NOTICE` and the
measurement/normalizer versions it was computed against, so a threshold used
downstream can always be traced back to what it was tuned against.

## 4. What this means for reports

- A report may show a NeoMundi signal's mean and a Periscope-derived delta
  side by side, but they are always labeled distinctly (see
  `docs/REPORTING.md`).
- No report declares `safe`/`unsafe`, `compliant`/`non-compliant`, or a
  universal ranking of models — that is a policy decision, and policy
  belongs to the consuming organization, not to Periscope or to NeoMundi.
  See the NeoMundi Runtime Measurement Layer's `docs/CONSUMER_BOUNDARIES.md`
  for the full four-layer boundary (`Measurement != Interpretation != Policy
  != Execution`) this product operates under.
