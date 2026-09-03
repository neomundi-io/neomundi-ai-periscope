"""Public report 1: Executive Snapshot.

A short, decision-oriented brief for a technical lead, integrator or
executive. Answers: what was tested, what changed, where the strongest
variations are, which observations deserve further investigation, what the
principal operational signals are, and what the limitations are.

"Measured signal, not verdict": this report never certifies, never declares
safe/unsafe or compliant/non-compliant, and never produces a universal
ranking of models.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from periscope.analysis.audit import run_audit
from periscope.analysis.finops import analyze_finops
from periscope.analysis.variability import analyze_variability
from periscope.datasets.canonicalize import CanonicalDataset
from periscope.export.manifest import CampaignManifest
from periscope.reports.common.charts import grouped_bar_chart
from periscope.reports.common.html import esc, fmt_int, fmt_number, html_doc, metric_cards, table
from periscope.reports.common.localization import require_language
from periscope.reports.common.pdf import html_to_pdf
from periscope.reports.common.rendering import boundary_footer, campaign_meta_grid, report_header, simulated_notice_block

ENGINE_VERSION = "1.0.0"

LABELS = {
    "en": {
        "title": "AI Periscope — Executive Snapshot",
        "subtitle": "Fast decision brief: what was tested, what changed, and what deserves attention.",
        "what_tested": "What was tested",
        "operational_signals": "Principal operational signals",
        "strongest_variations": "Strongest variations",
        "strongest_variations_intro": "Prompts with the largest spread across the tested arms, ranked by stability spread.",
        "investigate": "Observations that deserve further investigation",
        "investigate_intro": "A Periscope-derived, descriptive review-priority heuristic -- not a NeoMundi signal and not an automated decision.",
        "limitations": "Limitations",
        "col_prompt": "Prompt",
        "col_spread": "Stability spread",
        "col_scope": "Scope",
        "col_priority": "Review priority",
        "col_flag_rate": "FLAG rate",
        "metric_observations": "observations",
        "metric_stability": "mean stability",
        "metric_factual": "mean factual-risk signal",
        "metric_semantic": "mean semantic instability",
        "metric_latency": "mean latency (ms)",
        "metric_tokens": "mean tokens",
    },
    "fr": {
        "title": "AI Periscope — Snapshot exécutif",
        "subtitle": "Brief de décision rapide : ce qui a été testé, ce qui a changé, et ce qui mérite attention.",
        "what_tested": "Ce qui a été testé",
        "operational_signals": "Principaux signaux opérationnels",
        "strongest_variations": "Variations les plus fortes",
        "strongest_variations_intro": "Prompts présentant la plus forte amplitude entre les arms testés, classés par amplitude de stabilité.",
        "investigate": "Observations méritant une investigation complémentaire",
        "investigate_intro": "Heuristique de priorisation descriptive Periscope -- pas un signal NeoMundi, pas une décision automatisée.",
        "limitations": "Limites",
        "col_prompt": "Prompt",
        "col_spread": "Amplitude de stabilité",
        "col_scope": "Périmètre",
        "col_priority": "Priorité de revue",
        "col_flag_rate": "Taux FLAG",
        "metric_observations": "observations",
        "metric_stability": "stabilité moyenne",
        "metric_factual": "signal de risque factuel moyen",
        "metric_semantic": "instabilité sémantique moyenne",
        "metric_latency": "latence moyenne (ms)",
        "metric_tokens": "tokens moyens",
    },
}

LIMITATIONS = {
    "en": [
        "This snapshot summarizes signals; it does not constitute a factual verdict, safety certification, or compliance conclusion.",
        "Results apply only to the documented corpus, provider(s), model(s), repetitions and measurement version(s).",
        "Review-priority levels are a Periscope-side heuristic, not an official NeoMundi threshold.",
        "See the Model Release Benchmark report for a fuller cross-arm comparison, and docs/REPORT_LIBRARY.md for advanced reports available on request.",
    ],
    "fr": [
        "Ce snapshot résume des signaux ; il ne constitue ni un verdict factuel, ni une certification de sécurité, ni une conclusion de conformité.",
        "Les résultats valent uniquement pour le corpus, le(s) provider(s), le(s) modèle(s), les répétitions et la (les) version(s) de mesure documentés.",
        "Les niveaux de priorité de revue sont une heuristique Periscope, pas un seuil officiel NeoMundi.",
        "Voir le rapport Model Release Benchmark pour une comparaison inter-arms plus complète, et docs/REPORT_LIBRARY.md pour les rapports avancés disponibles sur demande.",
    ],
}


@dataclass
class ExecutiveSnapshotResult:
    html_path: Path
    pdf_path: Path | None
    pdf_engine: str | None


def _render(canonical: CanonicalDataset, manifest: CampaignManifest, lang: str, logos: dict) -> str:
    L = LABELS[lang]
    variability = analyze_variability(canonical)
    finops = analyze_finops(canonical)
    audit = run_audit(canonical)

    body = report_header(L["title"], L["subtitle"], lang, logos.get("neomundi_logo"), logos.get("org_name", ""), logos.get("org_logo"))
    body += simulated_notice_block(manifest, lang)

    body += f"<h2>{esc(L['what_tested'])}</h2>" + campaign_meta_grid(manifest, lang)

    dist = variability.metric_distributions
    body += f"<h2>{esc(L['operational_signals'])}</h2>"
    body += metric_cards(
        [
            (fmt_int(manifest.observation_count), L["metric_observations"]),
            (fmt_number(dist["nm_stability_score"]["mean"]), L["metric_stability"]),
            (fmt_number(dist["nm_factual_hallucination_score"]["mean"]), L["metric_factual"]),
            (fmt_number(dist["nm_semantic_instability_score"]["mean"]), L["metric_semantic"]),
            (fmt_number(finops.latency_ms["mean"], 1), L["metric_latency"]),
            (fmt_number(finops.token_count["mean"], 1), L["metric_tokens"]),
        ]
    )

    if len(manifest.arms) >= 2:
        arm_means = {arm: [canonical_mean(canonical, arm, "nm_stability_score")] for arm in manifest.arms}
        body += grouped_bar_chart(["stability"], arm_means)

    body += f"<h2>{esc(L['strongest_variations'])}</h2><p>{esc(L['strongest_variations_intro'])}</p>"
    rows = [
        [r["prompt_id"], (r["prompt_text"] or "")[:70], fmt_number(r["spread"])]
        for r in variability.most_variable_prompts
    ]
    body += table([L["col_prompt"], L["col_prompt"] + " (text)", L["col_spread"]], rows) if rows else "<p><em>—</em></p>"

    body += f"<h2>{esc(L['investigate'])}</h2><p>{esc(L['investigate_intro'])}</p>"
    audit_rows = [
        [f.scope, f.review_priority, fmt_number(f.flag_rate, 2), fmt_int(f.observation_count)]
        for f in audit.findings
    ]
    body += table([L["col_scope"], L["col_priority"], L["col_flag_rate"], L["metric_observations"]], audit_rows)

    body += f"<h2>{esc(L['limitations'])}</h2><ul>" + "".join(f"<li>{esc(item)}</li>" for item in LIMITATIONS[lang]) + "</ul>"

    body += boundary_footer(lang, ENGINE_VERSION)
    return html_doc(L["title"], body, lang)


def canonical_mean(canonical: CanonicalDataset, arm_id: str, column: str) -> float | None:
    from periscope.analysis._util import numeric_values, stats

    rows = [r for r in canonical.rows if r["id_arm_id"] == arm_id]
    return stats(numeric_values(rows, column))["mean"]


def generate_executive_snapshot(
    canonical: CanonicalDataset,
    manifest: CampaignManifest,
    output_dir: str | Path,
    lang: str = "en",
    organization_name: str = "",
    organization_logo: Path | None = None,
    neomundi_logo: Path | None = None,
    render_pdf: bool = True,
    pdf_engine: str = "auto",
) -> ExecutiveSnapshotResult:
    require_language(lang)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logos = {"neomundi_logo": neomundi_logo, "org_name": organization_name, "org_logo": organization_logo}
    html_content = _render(canonical, manifest, lang, logos)

    html_path = output_dir / f"executive_snapshot_{lang}.html"
    html_path.write_text(html_content, encoding="utf-8")

    pdf_path = None
    pdf_engine_used = None
    if render_pdf:
        candidate = output_dir / f"executive_snapshot_{lang}.pdf"
        ok, engine = html_to_pdf(html_path, candidate, pdf_engine)
        if ok:
            pdf_path = candidate
            pdf_engine_used = engine

    return ExecutiveSnapshotResult(html_path=html_path, pdf_path=pdf_path, pdf_engine=pdf_engine_used)
