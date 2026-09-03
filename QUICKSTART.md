# Quickstart

## 1. Install

```bash
python -m pip install -e .
# or, without installing the package:
python -m pip install -r requirements.txt
```

Optional, for PDF report generation (either is enough):

```bash
python -m pip install playwright && python -m playwright install chromium
# or
python -m pip install weasyprint
```

## 2. Try it with no API keys (offline simulator)

```bash
periscope run examples/campaigns/sample_campaign.yaml --simulate
```

This runs the bundled sample corpus (`examples/datasets/sample_prompts.csv`)
against two simulated arms, 3 repetitions each, and writes a canonical
dataset + manifest to `examples/outputs/sample_release_check/`. Every
observation is marked `synthetic: true`; reports generated from it carry an
explicit "synthetic data" notice.

## 3. Generate the two open reports

```bash
periscope report sample_release_check --type snapshot --lang both
periscope report sample_release_check --type model-release-benchmark --lang both
```

Output lands in `examples/outputs/sample_release_check/reports/` — HTML
always, plus PDF when Playwright or WeasyPrint is installed.

## 4. Run it for real

1. Get a NeoMundi API key.
2. Get an API key from each provider you want to test (see the [supported
   provider list](./docs/CAMPAIGN_MODEL.md#providers)).
3. Export them as environment variables — never paste them into a config
   file:

```bash
export NEOMUNDI_API_KEY=...
export PERISCOPE_OPENAI_API_KEY=...
export PERISCOPE_ANTHROPIC_API_KEY=...
```

4. Write your own dataset (CSV or JSON — see
   [`examples/datasets/sample_prompts.csv`](./examples/datasets/sample_prompts.csv))
   and campaign file (see
   [`examples/campaigns/sample_campaign.yaml`](./examples/campaigns/sample_campaign.yaml)).
5. Run it:

```bash
periscope run my_campaign.yaml
periscope report my_campaign_id --type model-release-benchmark --lang en
```

## The seven-step golden path

1. Select a CSV/JSON dataset.
2. Choose provider(s)/model(s).
3. Choose repetitions.
4. Run the campaign.
5. Get the canonical dataset (`campaign_results.json` / `.csv`).
6. Generate a benchmark or snapshot.
7. Read the report.

## Where to go next

- [`docs/CAMPAIGN_MODEL.md`](./docs/CAMPAIGN_MODEL.md) — the full
  `campaign.yaml` schema.
- [`docs/REPORTING.md`](./docs/REPORTING.md) — what each open report covers.
- [`docs/REPORT_LIBRARY.md`](./docs/REPORT_LIBRARY.md) — advanced reports
  available on request.
- [`docs/METRIC_BOUNDARIES.md`](./docs/METRIC_BOUNDARIES.md) — how NeoMundi
  measurements, campaign operational data, and Periscope analysis stay
  separated.
