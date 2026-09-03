"""Campaign configuration: what a campaign.yaml file declares.

A campaign is 1 dataset x N (provider, model) arms x N repetitions, without
duplicating the engine per provider or per model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

from periscope.providers.adapter import ProviderModelArm


class CampaignConfigError(ValueError):
    pass


@dataclass(frozen=True)
class CampaignConfig:
    campaign_id: str
    dataset_path: str
    arms: tuple[ProviderModelArm, ...]
    repetitions: int
    output_dir: str
    measurement_mode: str = "OBS"
    schema_version_preference: str | None = None
    baseline_arm_id: str | None = None
    notes: str = ""
    created_at_utc: str = ""

    @property
    def dataset_id(self) -> str:
        return Path(self.dataset_path).stem


REQUIRED_FIELDS = ("dataset", "providers_models", "repetitions")


def _default_campaign_id() -> str:
    return "cmp_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def load_campaign_config(path: str | Path) -> CampaignConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Campaign file not found: {path}")

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise CampaignConfigError(f"{path} is empty or is not a mapping.")

    missing = [f for f in REQUIRED_FIELDS if raw.get(f) in (None, "", [])]
    if missing:
        raise CampaignConfigError(f"Missing required field(s) in {path}: {missing}")

    arms_raw = raw["providers_models"]
    if not isinstance(arms_raw, list) or not arms_raw:
        raise CampaignConfigError("'providers_models' must be a non-empty list of {provider, model}.")

    arms = []
    for i, entry in enumerate(arms_raw):
        if not isinstance(entry, dict) or "provider" not in entry or "model" not in entry:
            raise CampaignConfigError(f"providers_models[{i}] must have 'provider' and 'model'.")
        arms.append(ProviderModelArm(provider=str(entry["provider"]), model=str(entry["model"])))

    repetitions = int(raw["repetitions"])
    if repetitions < 1:
        raise CampaignConfigError("'repetitions' must be at least 1.")

    measurement_cfg = raw.get("measurement") or {}
    if not isinstance(measurement_cfg, dict):
        raise CampaignConfigError("'measurement' must be a mapping if present.")

    dataset_path = str(raw["dataset"])
    output_dir = str(raw.get("output_dir") or "examples/outputs")

    return CampaignConfig(
        campaign_id=str(raw.get("campaign_id") or _default_campaign_id()),
        dataset_path=dataset_path,
        arms=tuple(arms),
        repetitions=repetitions,
        output_dir=output_dir,
        measurement_mode=str(measurement_cfg.get("mode") or "OBS"),
        schema_version_preference=measurement_cfg.get("schema_version_preference"),
        baseline_arm_id=raw.get("baseline_arm_id"),
        notes=str(raw.get("notes") or ""),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
    )
