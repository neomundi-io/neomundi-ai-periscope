# Benchmark

`periscope.analysis.benchmark.build_benchmark(dataset, reference_arm_id=None)`
is the analysis backbone of the **Model Release Benchmark Report** (see
[REPORTING.md](./REPORTING.md)): it composes baselines, arm comparisons,
repeatability and prompt-level variation for every arm present in a
canonical dataset.

```python
from periscope.analysis.benchmark import build_benchmark

result = build_benchmark(canonical, reference_arm_id="openai:gpt-4o-2024-11-20")
result.baselines_by_arm      # {arm_id: Baseline}
result.arm_comparison        # ComparisonTable, deltas vs reference_arm_id
result.repeatability         # RepeatabilityReport across all arms
result.prompt_level_variation  # per-prompt spread across arms
```

## Comparison primitives (`periscope.analysis.comparison`)

| Function | Groups by |
|---|---|
| `compare_runs(datasets, reference_campaign_id=None)` | campaign (multiple canonical datasets, e.g. two campaigns over time) |
| `compare_models(dataset, reference_model=None)` | `id_model` |
| `compare_providers(dataset, reference_provider=None)` | `id_provider` |
| `compare_arms(dataset, reference_arm_id=None)` | `id_arm_id` (provider+model pair) |
| `analyze_prompt_level_variation(dataset, metric=...)` | per-prompt spread across arms |

Every comparison reports a **measured delta relative to an explicit
reference group** — never an implicit ranking. If no reference is given, the
first group alphabetically is used and stated explicitly
(`ComparisonTable.reference_group`).

## This is not a universal leaderboard

`BenchmarkResult.notice` and every rendering of it states this explicitly.
The product never outputs "Model X is the best model." It outputs, e.g.:

> Under this dataset, protocol and measurement version, `anthropic:claude-sonnet-5`
> showed a stability delta of -0.019 and a token-count delta of +13.5 versus
> `openai:gpt-4o-2024-11-20`.

Scope is always explicit: results apply to the tested corpus, provider(s),
model(s), repetitions, measurement version(s), and time period only — see
`docs/REPORT_LIBRARY.md` and the reproducibility manifest section of every
benchmark report.

## Use cases

Model release evaluation, provider comparison, migration assessment, model
version change, pre-production baseline, post-upgrade comparison — run the
same corpus through the new arm and an existing baseline arm in one
campaign, then `periscope report <campaign> --type model-release-benchmark`.
