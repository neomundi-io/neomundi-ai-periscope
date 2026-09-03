"""Shared report chrome: header, scope statement, and the interpretation
boundary footer every open report must carry, from one implementation so
the two reports can never drift apart on this wording.
"""

from __future__ import annotations

from pathlib import Path

from periscope.export.manifest import CampaignManifest
from periscope.reports.common.html import brands_block, esc, meta_grid
from periscope.reports.common.localization import t


def report_header(
    title: str,
    subtitle: str,
    lang: str,
    neomundi_logo: Path | None = None,
    org_name: str = "",
    org_logo: Path | None = None,
) -> str:
    return (
        brands_block(neomundi_logo, org_name, org_logo)
        + f"<h1>{esc(title)}</h1>"
        + f'<div class="subtitle">{esc(subtitle)}</div>'
    )


def campaign_meta_grid(manifest: CampaignManifest, lang: str) -> str:
    items = [
        (t(lang, "campaign_id"), manifest.campaign_id),
        (t(lang, "dataset"), manifest.dataset_id),
        (t(lang, "arms_tested"), ", ".join(manifest.arms)),
        (t(lang, "repetitions"), manifest.repetitions),
        (t(lang, "observations"), manifest.observation_count),
        (t(lang, "errors"), manifest.error_count),
        (t(lang, "measurement_schema_versions"), ", ".join(manifest.measurement_schema_versions) or t(lang, "na")),
        (t(lang, "measurement_engine_versions"), ", ".join(manifest.measurement_engine_versions) or t(lang, "na")),
        (t(lang, "generated"), manifest.generated_at_utc),
    ]
    return meta_grid(items)


def simulated_notice_block(manifest: CampaignManifest, lang: str) -> str:
    if not manifest.simulated:
        return ""
    return f'<div class="callout"><strong>{esc(t(lang, "simulated_notice"))}</strong></div>'


def boundary_footer(lang: str, engine_version: str) -> str:
    return (
        f'<div class="boundary"><strong>{esc(t(lang, "boundary_title"))}</strong><br>'
        f"{esc(t(lang, 'boundary_text'))}</div>"
        f'<div class="footer"><div>{esc(t(lang, "footer_engine"))} v{esc(engine_version)}</div>'
        f"<div>NeoMundi Research</div></div>"
    )
