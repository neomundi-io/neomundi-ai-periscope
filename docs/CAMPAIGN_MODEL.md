# Campaign Model

A campaign is `1 dataset x N (provider, model) arms x N repetitions`,
executed by one engine (`periscope.campaign.runner.run_campaign`) without
duplicating that engine per provider or per model.

## Minimum fields (`campaign.yaml`)

```yaml
campaign_id: sample_release_check       # optional; auto-generated if omitted

dataset: examples/datasets/sample_prompts.csv   # CSV or JSON prompt corpus

providers_models:                        # >= 1 (provider, model) arm
  - provider: openai
    model: gpt-4o-2024-11-20
  - provider: anthropic
    model: claude-sonnet-5

repetitions: 3                           # >= 1, applied to every arm

baseline_arm_id: "openai:gpt-4o-2024-11-20"   # optional: default reference
                                               # arm for benchmark reports

measurement:
  mode: OBS                              # passed through to /v1/govern
  schema_version_preference: "0.2.0"     # informational; both 0.1.0 and
                                          # 0.2.0 responses are handled

output_dir: examples/outputs

notes: "free-text context for this campaign"
```

See `periscope/campaign/configuration.py` for the loader and validation
(`CampaignConfigError` on missing/invalid fields) and
`examples/campaigns/sample_campaign.yaml` for a runnable example.

## Execution plan

`periscope/campaign/repetition.py::build_execution_plan` expands a
`CampaignConfig` and a loaded prompt list into a flat list of
`ExecutionUnit(prompt, arm, repetition_index, planned_repetitions)` —
`len(prompts) * len(arms) * repetitions` units, in that nesting order
(prompt, then arm, then repetition).

## Running a campaign

```bash
# Offline demo / test, no API keys required:
periscope run examples/campaigns/sample_campaign.yaml --simulate

# Against live NeoMundi + provider APIs:
export NEOMUNDI_API_KEY=...
export PERISCOPE_OPENAI_API_KEY=...
export PERISCOPE_ANTHROPIC_API_KEY=...
periscope run examples/campaigns/sample_campaign.yaml
```

Each provider's key is read from a dedicated environment variable
(`PERISCOPE_<PROVIDER>_API_KEY`, see `periscope/providers/registry.py`) —
never written into a config file or a script, unlike the legacy launcher
this product replaces.

`run_campaign()` checkpoints (rewrites `campaign_results.json` and
`campaign_results.csv`) after **every** observation, so an interrupted
campaign still leaves a usable, consistent canonical dataset. On completion
it writes `campaign_manifest.json` — see
[the reproducibility section of REPORTING.md](./REPORTING.md).

## Providers

Only providers documented by NeoMundi's own integration guide are
supported (`periscope/providers/registry.py`, sourced from
`API_INTEGRATION_GUIDE.md` section 3.1):

```text
openai · anthropic · google (alias gemini) · mistral · cohere · deepseek
xai (alias grok) · perplexity · together · qwen · apertus · euria
```

No provider-specific logic lives in the core engine — every documented
provider is called through the same NeoMundi `/v1/govern/stream` payload
shape (`periscope/providers/adapter.py`).

## The offline simulator

`periscope.measurement.simulated.SimulatedMeasurementClient` is a
deterministic, network-free stand-in for the real NeoMundi client, used by
the automated test suite and available to anyone trying the product before
they have credentials (`--simulate` on the CLI). Every record it produces is
marked `synthetic: true`, and a campaign run with `--simulate` propagates
`simulated: true` into the manifest — reports generated from it carry an
explicit "synthetic data" notice (see `docs/REPORTING.md`).
