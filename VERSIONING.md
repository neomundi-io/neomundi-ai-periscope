# Versioning

Two independent version spaces matter here. AI Periscope tracks the second;
it does not own it.

## 1. AI Periscope Layer version (`periscope.__version__`)

Standard [semantic versioning](https://semver.org/) for this package
(`pyproject.toml`, `periscope/__init__.py`). Current: `1.0.0`.

- **Major** — breaking change to the canonical dataset schema, the campaign
  config schema, or a public report's structure.
- **Minor** — new analysis function, new report type, new provider added to
  the registry (as NeoMundi documents it), backward-compatible CLI addition.
- **Patch** — bug fixes, doc updates, no schema/behavior change.

## 2. NeoMundi measurement versions (not owned by this repository)

Every canonical dataset row records, verbatim from the NeoMundi API
response, the versions it was measured under:

- `nm_schema_version` — the RGC contract schema version (`0.1.0` or `0.2.0`
  in this build; see `periscope/measurement/contracts.py`,
  `SUPPORTED_SCHEMA_VERSIONS`).
- `nm_measurement_version` — NeoMundi's measurement engine version.
- `nm_normalizer_version` — NeoMundi's normalizer version.

A `campaign_manifest.json` aggregates the distinct versions observed across
a campaign (`measurement_schema_versions`, `measurement_engine_versions`),
so a report or a downstream consumer can tell at a glance whether a campaign
mixed measurement versions.

**Never compare across measurement versions silently.** If NeoMundi's
measurement or normalizer version changes between two campaigns, treat that
as a documented condition of the comparison, not an implementation detail —
`analysis.comparison.compare_runs` does not itself detect or warn about a
version change; check `campaign_manifest.json` on both sides before trusting
a longitudinal or benchmark delta across campaigns run at different times.

## Adding a new supported RGC schema version

1. Add it to `SUPPORTED_SCHEMA_VERSIONS` in `periscope/measurement/contracts.py`.
2. Extend `periscope/measurement/runtime.py::build_measurement_record` if the
   new version changes field paths or adds new normative consistency rules
   (mirroring what v0.2 added over v0.1 — per-signal `signal_status`,
   coverage/status consistency).
3. Add a test in `tests/test_measurement_boundaries.py` exercising the new
   version's specific rules.
