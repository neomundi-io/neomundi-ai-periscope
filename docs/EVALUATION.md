# Evaluation

`periscope.analysis.evaluation.run_evaluation(dataset, manifest)` produces a
structured `EvaluationSummary`: corpus, protocol, observation counts,
excluded observations, and known limitations — the reproducibility record
a third party needs to understand and challenge a campaign.

```python
from periscope.analysis.evaluation import run_evaluation

summary = run_evaluation(canonical, manifest)
summary.excluded_observations   # every execution error, with prompt/arm/repetition/reason
summary.known_limitations       # the product's standing interpretation limits
```

No exclusion is hidden: `excluded_observations` lists every observation that
errored during execution, with its prompt, arm, repetition index, and error
reason — mirroring the "no masked exclusions" principle from the
methodological reference (`source_selection_log.csv` /
`baro_excluded_rows` in the Euria generator).

## Relationship to the Audit / Evaluation Report

A full **Audit / Evaluation Report** documenting corpus, protocol,
observations, anomalies, limits, and items requiring review as one
narrative document is available on request — see
[REPORT_LIBRARY.md](./REPORT_LIBRARY.md). `run_evaluation` is the data this
report would be built from; it is not yet packaged as a standalone public
report generator in this build.
