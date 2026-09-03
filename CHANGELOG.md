# Changelog

## 1.0.0 — 2026-09-03

Full rebuild of NeoMundi AI Periscope as a campaign / benchmark / baseline /
evaluation engine on top of the NeoMundi Runtime Measurement Layer, with an
open Report Library.

### Added

- Campaign engine: `1 dataset x N provider/model arms x N repetitions` in
  one execution plan (`periscope.campaign`), replacing the previous
  single-provider, single-model `config.yaml` + `periscope.py` launcher.
- Provider registry sourced from NeoMundi's documented provider list
  (`periscope.providers`), with per-provider API keys read from dedicated
  environment variables instead of being pasted into a script.
- NeoMundi measurement client implementing the documented 3-step flow
  (`/v1/govern/stream` -> `/v1/govern` -> optional `/v1/rgc/contracts/{id}`),
  plus a deterministic offline simulator for tests and credential-free demos
  (`periscope.measurement`).
- Structural RGC v0.1 / v0.2 handling: per-signal `measured` /
  `not_measured` / `insufficient_coverage` status, coverage/status
  consistency checks, no missing signal ever silently defaulted to 0.
- Canonical dataset with a strict `id_*` / `nm_*` / `op_*` column namespace
  (`periscope.datasets.canonicalize`) and a campaign manifest with file
  hashes, measurement versions, and error counts (`periscope.export.manifest`).
- Full analysis library: `build_baseline`, `compare_runs` /
  `compare_models` / `compare_providers` / `compare_arms`,
  `analyze_prompt_level_variation`, `analyze_repeatability`,
  `analyze_variability`, `analyze_longitudinal_change`, `analyze_finops`,
  `run_audit`, `run_evaluation`, `build_benchmark` (`periscope.analysis`).
- Two public reports, HTML + PDF, FR + EN: **Executive Snapshot** and
  **Model Release Benchmark Report** (`periscope.reports.open`), built on
  dependency-free shared rendering/chart/localization/PDF infrastructure
  (`periscope.reports.common`).
- `docs/REPORT_LIBRARY.md` documenting six additional report types
  available on request, and `periscope/reports/advanced/README.md`
  explaining why they are not shipped as public generators in this build.
- CLI: `periscope run campaign.yaml [--simulate]`,
  `periscope report <campaign> --type snapshot|model-release-benchmark`.
- Automated test suite covering dataset validation, single/multi-model,
  multi-provider campaigns, partial/missing NeoMundi measurements, report
  generation (HTML + PDF, FR + EN), canonical dataset consistency, and the
  NeoMundi-measurement-vs-Periscope-analysis boundary.

### Removed

- `RUN_PERISCOPE.ps1` (Windows-only launcher storing API keys in plain
  text), `periscope.py`, `snapshot.py`, `config.yaml`, `prompts.txt`,
  `.env.example` — superseded by the campaign engine, CLI, and provider
  registry above. See the root `README.md` for the full audit of what was
  kept vs. abandoned from the previous version.

## 0.1.0 and earlier

See Git history prior to the 1.0.0 rebuild for the original single-provider
experimental launcher.
