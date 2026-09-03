# Advanced Report Library

This directory intentionally contains **no report generator code** in this
build.

The AI Periscope analysis library (`periscope/analysis/`) already computes
everything an advanced report needs — baselines, comparisons, repeatability,
variability, longitudinal series, audit/review findings, FinOps summaries.
What is not shipped here is the *rendering* layer that turns those analysis
outputs into a full report package (HTML/PDF, cover pages, multi-section
layout) for each advanced report type.

See [`docs/REPORT_LIBRARY.md`](../../../docs/REPORT_LIBRARY.md) for what
each advanced report covers and its availability.

## Why these are not public generators yet

- **Full Metrology Report**, **Governance / Review Report**, **FinOps
  Report** and **Longitudinal Report** exist as working, more elaborate
  implementations in NeoMundi's private methodological reference (the
  Euria/Fatima reporting generator). That code is client-specific and is
  not part of this public repository — see the root `README.md` section on
  private methodological references.
- **Compliance Evidence Report** and **Custom Report** are, by nature,
  specific to an external framework or a client's own requirements and are
  built on request rather than as a one-size-fits-all public generator.

## What is available now, without an advanced report

Everything in `periscope/analysis/` is public and usable directly, either
from Python or via the canonical JSON/CSV a campaign already produces:

- `analysis.baseline.build_baseline`
- `analysis.comparison.compare_runs / compare_models / compare_providers / compare_arms / analyze_prompt_level_variation`
- `analysis.repeatability.analyze_repeatability`
- `analysis.variability.analyze_variability`
- `analysis.longitudinal.analyze_longitudinal_change`
- `analysis.audit.run_audit`
- `analysis.evaluation.run_evaluation`
- `analysis.finops.analyze_finops`

A team comfortable with Python can build a custom report on top of these
functions and `periscope.reports.common` (HTML/PDF/localization/charts)
today. NeoMundi can also deliver a fully packaged advanced or custom report
on request — see the CTA in `docs/REPORT_LIBRARY.md`.
