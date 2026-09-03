"""Campaign manifest: what a third party needs to understand and reproduce a
campaign, per the product's reproducibility requirement.

A manifest states: corpus used, how many executions, which models/providers,
which measurement versions, when, and (via `simulated`) whether the
campaign used real NeoMundi measurements or the offline simulator. Nothing
is hidden -- in particular, error/excluded observations are counted, never
silently dropped from the manifest.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from periscope.campaign.configuration import CampaignConfig
from periscope.datasets.canonicalize import CanonicalDataset, utc_now_iso


def _file_sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass
class CampaignManifest:
    campaign_id: str
    generated_at_utc: str
    dataset_path: str
    dataset_id: str
    dataset_sha256: str | None
    arms: list[str]
    repetitions: int
    observation_count: int
    error_count: int
    measurement_schema_versions: list[str]
    measurement_engine_versions: list[str]
    canonical_payload_hash: str
    simulated: bool
    notes: str
    baseline_arm_id: str | None = None
    output_files_sha256: dict[str, str] = field(default_factory=dict)


def build_manifest(
    config: CampaignConfig,
    canonical: CanonicalDataset,
    simulated: bool,
    output_dir: Path,
) -> CampaignManifest:
    schema_versions = sorted(
        {str(row["nm_schema_version"]) for row in canonical.rows if row.get("nm_schema_version")}
    )
    engine_versions = sorted(
        {str(row["nm_measurement_version"]) for row in canonical.rows if row.get("nm_measurement_version")}
    )

    output_files_sha256 = {}
    for name in ("campaign_results.json", "campaign_results.csv"):
        digest = _file_sha256(output_dir / name)
        if digest:
            output_files_sha256[name] = digest

    return CampaignManifest(
        campaign_id=config.campaign_id,
        generated_at_utc=utc_now_iso(),
        dataset_path=config.dataset_path,
        dataset_id=config.dataset_id,
        dataset_sha256=_file_sha256(Path(config.dataset_path)),
        arms=[arm.arm_id for arm in config.arms],
        repetitions=config.repetitions,
        observation_count=canonical.observation_count,
        error_count=canonical.error_count,
        measurement_schema_versions=schema_versions,
        measurement_engine_versions=engine_versions,
        canonical_payload_hash=canonical.payload_hash(),
        simulated=simulated,
        notes=config.notes,
        baseline_arm_id=config.baseline_arm_id,
        output_files_sha256=output_files_sha256,
    )


def write_manifest(manifest: CampaignManifest, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(manifest), ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_manifest(path: str | Path) -> CampaignManifest:
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    return CampaignManifest(**data)
