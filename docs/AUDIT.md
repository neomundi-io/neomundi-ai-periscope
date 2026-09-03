# Audit

`periscope.analysis.audit.run_audit(dataset, thresholds=DEFAULT_THRESHOLDS)`
turns measured signals into review-priority objects — a **descriptive
prioritization heuristic**, not a NeoMundi signal and not an automated
decision. Full context in [METRIC_BOUNDARIES.md](./METRIC_BOUNDARIES.md).

```python
from periscope.analysis.audit import run_audit, AuditThresholds

report = run_audit(canonical)   # default thresholds
report = run_audit(canonical, thresholds=AuditThresholds(flag_rate_high=0.15))
```

Each `AuditFinding` (currently scoped per arm) carries:

- `flag_rate` — share of `nm_decision == "FLAG"` observations
- `factual_hallucination_mean`, `semantic_instability_mean`
- `error_count` — execution errors, never silently dropped
- `review_priority` — `HIGH_REVIEW` / `REVIEW` / `ROUTINE`
- `interpretation_boundary` — a fixed disclaimer string carried on every finding

`AuditReport.thresholds_notice` states explicitly, on every audit result:

> NeoMundi does not publish official numeric thresholds for its signals. Any
> threshold used below is a Periscope-side, campaign-specific configuration
> choice — not a NeoMundi norm.

## Default thresholds

```python
flag_rate_high = 0.10            flag_rate_review = 0.0
factual_risk_high = 0.05         factual_risk_review = 0.01
semantic_instability_high = 0.05 semantic_instability_review = 0.01
```

These defaults are carried over, as a **starting point only**, from
NeoMundi's private Euria/Fatima methodological reference. They are not
validated NeoMundi norms and should be tuned per campaign, domain, and risk
appetite before being used for anything beyond a first pass.

## Where this shows up today

The **Executive Snapshot** surfaces `run_audit` findings under "Observations
that deserve further investigation." A full **Governance / Review Report**
with a priority map, an interpretation grammar, and a documented
action-rule table is available on request — see
[REPORT_LIBRARY.md](./REPORT_LIBRARY.md).
