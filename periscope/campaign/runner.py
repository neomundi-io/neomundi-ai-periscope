"""run_campaign(): the single engine every Periscope use case sits on top of.

    dataset -> execution plan -> NeoMundi measurement (per unit) -> canonical dataset

Benchmark, baseline, audit, evaluation and every report are views/functions
computed afterwards from the canonical dataset -- they never re-run the
campaign or recompute a NeoMundi measurement differently.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from periscope.campaign.configuration import CampaignConfig, load_campaign_config
from periscope.campaign.repetition import ExecutionUnit, build_execution_plan
from periscope.datasets.canonicalize import CanonicalDataset, Observation, build_canonical_dataset, utc_now_iso
from periscope.datasets.loader import load_dataset
from periscope.datasets.validation import require_valid
from periscope.export.manifest import CampaignManifest, build_manifest, write_manifest
from periscope.export.csv_export import write_canonical_csv
from periscope.export.json_export import write_canonical_json
from periscope.measurement.client import MeasurementResult
from periscope.providers.adapter import resolve_provider_api_key


class MeasurementClient(Protocol):
    def measure(
        self, prompt: str, arm, provider_api_key: str | None, seed_key: str
    ) -> MeasurementResult: ...


@dataclass
class CampaignRunResult:
    config: CampaignConfig
    canonical_dataset: CanonicalDataset
    manifest: CampaignManifest
    output_dir: Path


def _execute_unit(
    config: CampaignConfig,
    unit: ExecutionUnit,
    client: MeasurementClient,
    provider_api_key: str | None,
) -> Observation:
    seed_key = f"{unit.prompt.prompt_id}:{unit.arm.arm_id}:{unit.repetition_index}"
    result = client.measure(unit.prompt.prompt, unit.arm, provider_api_key, seed_key)

    return Observation(
        campaign_id=config.campaign_id,
        dataset_id=config.dataset_id,
        prompt_id=unit.prompt.prompt_id,
        prompt=unit.prompt.prompt,
        prompt_family=unit.prompt.prompt_family,
        domain=unit.prompt.domain,
        provider=unit.arm.provider,
        model=unit.arm.model,
        arm_id=unit.arm.arm_id,
        repetition_index=unit.repetition_index,
        planned_repetitions=unit.planned_repetitions,
        timestamp_utc=utc_now_iso(),
        measurement=result.measurement,
        latency_ms=result.latency_ms,
        token_count=result.token_count,
        error=result.error,
    )


def run_campaign(
    config_path: str | Path,
    client: MeasurementClient,
    simulated: bool = False,
    progress_callback=None,
) -> CampaignRunResult:
    """Run a full campaign and return its canonical dataset + manifest.

    `client` is injected so the same engine runs against the real NeoMundi
    API or a deterministic offline SimulatedMeasurementClient (used by tests
    and demos) without any branching in this function.

    Results are checkpointed (JSON + CSV rewritten) after every observation,
    so a campaign interrupted partway through still leaves a usable,
    consistent canonical dataset on disk.
    """
    config = load_campaign_config(config_path)
    prompts = load_dataset(config.dataset_path)
    require_valid(prompts)

    plan = build_execution_plan(config, prompts)

    campaign_dir = Path(config.output_dir) / config.campaign_id
    campaign_dir.mkdir(parents=True, exist_ok=True)

    # Resolve one provider API key per distinct provider up front.
    api_keys: dict[str, str | None] = {}
    if not simulated:
        for arm in config.arms:
            if arm.provider not in api_keys:
                api_keys[arm.provider] = resolve_provider_api_key(arm.provider)

    observations: list[Observation] = []
    for index, unit in enumerate(plan, start=1):
        provider_api_key = None if simulated else api_keys.get(unit.arm.provider)
        observation = _execute_unit(config, unit, client, provider_api_key)
        observations.append(observation)

        if progress_callback:
            progress_callback(index, len(plan), observation)

        # Checkpoint after every observation.
        canonical = build_canonical_dataset(config.campaign_id, observations)
        write_canonical_json(canonical, campaign_dir / "campaign_results.json")
        write_canonical_csv(canonical, campaign_dir / "campaign_results.csv")

    canonical = build_canonical_dataset(config.campaign_id, observations)
    manifest = build_manifest(config=config, canonical=canonical, simulated=simulated, output_dir=campaign_dir)
    write_manifest(manifest, campaign_dir / "campaign_manifest.json")

    return CampaignRunResult(config=config, canonical_dataset=canonical, manifest=manifest, output_dir=campaign_dir)
