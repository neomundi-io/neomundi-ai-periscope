"""Public report 2: Model Release Benchmark Report.

For teams evaluating a newly released model against an existing baseline, a
previous model version, competing models, or multiple providers, on the
same corpus and protocol.

This is NOT a universal leaderboard. It never states "Model X is the best
model" -- it states measured deltas under a documented corpus, protocol and
measurement version, and leaves interpretation to the reader.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from periscope.analysis._util import numeric_values, stats
from periscope.analysis.benchmark import BenchmarkResult, build_benchmark
from periscope.analysis.finops import FinOpsReport, PriceTable, analyze_finops
from periscope.datasets.canonicalize import CanonicalDataset
from periscope.export.manifest import CampaignManifest
from periscope.reports.common.charts import grouped_bar_chart
from periscope.reports.common.html import esc, fmt_int, fmt_number, fmt_signed_percent, html_doc, metric_cards, table
from periscope.reports.common.localization import require_language
from periscope.reports.common.pdf import html_to_pdf
from periscope.reports.common.rendering import boundary_footer, campaign_meta_grid, report_header, simulated_notice_block

ENGINE_VERSION = "1.0.0"

BEHAVIOURAL_METRICS = (
    ("nm_stability_score", {"en": "Stability", "fr": "Stabilité"}),
    ("nm_coherence_score", {"en": "Coherence", "fr": "Cohérence"}),
    ("nm_factual_hallucination_score", {"en": "Factual-risk signal", "fr": "Signal de risque factuel"}),
    ("nm_semantic_instability_score", {"en": "Semantic instability", "fr": "Instabilité sémantique"}),
    ("nm_semantic_risk", {"en": "Semantic risk", "fr": "Risque sémantique"}),
)
OPERATIONAL_METRICS = (
    ("op_latency_ms", {"en": "Latency (ms)", "fr": "Latence (ms)"}),
    ("op_token_count", {"en": "Tokens", "fr": "Tokens"}),
)

LABELS = {
    "en": {
        "title": "AI Periscope — Model Release Benchmark Report",
        "subtitle": "Compare a newly released model against a baseline, a previous version, or peers, on the same corpus and protocol.",
        "not_a_leaderboard": "This is not a universal leaderboard. Values below describe what was measured on this corpus, protocol and measurement version -- not a claim that one arm is universally 'better'.",
        "s_protocol": "1. Test protocol",
        "s_dataset": "2. Dataset / corpus",
        "s_models": "3. Models and providers tested",
        "s_runs": "4. Runs / repetitions",
        "s_versions": "5. Measurement versions",
        "s_behavioural": "6. Behavioural comparison",
        "s_stability": "7. Stability / variability",
        "s_factual": "8. Factual-risk signals",
        "s_semantic": "9. Semantic / coherence signals",
        "s_latency_tokens": "10. Latency / tokens",
        "s_density": "11. Information density",
        "s_density_note": "Not part of the current canonical measurement schema for this campaign -- not reported.",
        "s_cost": "12. Cost / energy-related fields",
        "s_cost_note_no_table": "No dated, versioned price table was supplied for this report -- cost is not estimated. Token and latency signals are shown above as efficiency proxies.",
        "s_cost_note_table": "Estimated from the supplied price table below. This is a Periscope-side estimate, not a NeoMundi signal.",
        "s_prompt_level": "13. Prompt-level differences",
        "s_distribution": "14. Distribution summary",
        "s_notable": "15. Notable changes",
        "s_limits": "16. Limits",
        "s_manifest": "17. Reproducibility manifest",
        "reference_arm": "Reference arm",
        "col_arm": "Arm",
        "col_metric": "Metric",
        "col_mean": "Mean",
        "col_delta": "Delta vs reference",
        "col_relative_delta": "Relative delta",
        "col_n": "N",
        "col_prompt": "Prompt",
        "col_spread": "Spread across arms",
        "col_file": "File",
        "col_sha256": "SHA-256",
        "col_stat": "Statistic",
        "col_value": "Value",
        "phrase_under": "Under this dataset, protocol and measurement version, the tested arms showed the differences below on the measured dimensions.",
    },
    "fr": {
        "title": "AI Periscope — Rapport de benchmark de sortie de modèle",
        "subtitle": "Comparer un modèle nouvellement publié à une baseline, une version précédente, ou des modèles pairs, sur le même corpus et protocole.",
        "not_a_leaderboard": "Ce rapport n'est pas un classement universel. Les valeurs ci-dessous décrivent ce qui a été mesuré sur ce corpus, ce protocole et cette version de mesure -- pas une affirmation qu'un arm est universellement « meilleur ».",
        "s_protocol": "1. Protocole de test",
        "s_dataset": "2. Dataset / corpus",
        "s_models": "3. Modèles et providers testés",
        "s_runs": "4. Exécutions / répétitions",
        "s_versions": "5. Versions de mesure",
        "s_behavioural": "6. Comparaison comportementale",
        "s_stability": "7. Stabilité / variabilité",
        "s_factual": "8. Signaux de risque factuel",
        "s_semantic": "9. Signaux sémantiques / cohérence",
        "s_latency_tokens": "10. Latence / tokens",
        "s_density": "11. Densité informationnelle",
        "s_density_note": "Ne fait pas partie du schéma de mesure canonique actuel pour cette campagne -- non rapporté.",
        "s_cost": "12. Champs coût / énergie",
        "s_cost_note_no_table": "Aucune table tarifaire datée et versionnée n'a été fournie pour ce rapport -- le coût n'est pas estimé. Les signaux de tokens et de latence sont présentés ci-dessus comme proxys d'efficacité.",
        "s_cost_note_table": "Estimé à partir de la table tarifaire fournie ci-dessous. Il s'agit d'une estimation Periscope, pas d'un signal NeoMundi.",
        "s_prompt_level": "13. Différences au niveau des prompts",
        "s_distribution": "14. Synthèse des distributions",
        "s_notable": "15. Changements notables",
        "s_limits": "16. Limites",
        "s_manifest": "17. Manifeste de reproductibilité",
        "reference_arm": "Arm de référence",
        "col_arm": "Arm",
        "col_metric": "Métrique",
        "col_mean": "Moyenne",
        "col_delta": "Delta vs référence",
        "col_relative_delta": "Delta relatif",
        "col_n": "N",
        "col_prompt": "Prompt",
        "col_spread": "Amplitude inter-arms",
        "col_file": "Fichier",
        "col_sha256": "SHA-256",
        "col_stat": "Statistique",
        "col_value": "Valeur",
        "phrase_under": "Sous ce dataset, ce protocole et cette version de mesure, les arms testés présentent les différences ci-dessous sur les dimensions mesurées.",
    },
}

LIMITATIONS = {
    "en": [
        "Results apply only to the tested corpus, provider(s), model(s), repetitions and measurement version(s) recorded in section 17.",
        "This report does not certify safety, compliance, or factual correctness, and does not produce a universal model ranking.",
        "A NeoMundi signal is a measurement, not a verdict -- see docs/METRIC_BOUNDARIES.md.",
        "Prompt-level differences reflect this corpus only and may not generalize to other corpora or task types.",
    ],
    "fr": [
        "Les résultats valent uniquement pour le corpus, le(s) provider(s), le(s) modèle(s), les répétitions et la (les) version(s) de mesure enregistrés en section 17.",
        "Ce rapport ne certifie ni la sécurité, ni la conformité, ni l'exactitude factuelle, et ne produit pas de classement universel des modèles.",
        "Un signal NeoMundi est une mesure, pas un verdict -- voir docs/METRIC_BOUNDARIES.md.",
        "Les différences au niveau des prompts ne reflètent que ce corpus et peuvent ne pas se généraliser à d'autres corpus ou types de tâches.",
    ],
}


@dataclass
class ModelReleaseBenchmarkResult:
    html_path: Path
    pdf_path: Path | None
    pdf_engine: str | None


def _metric_table(benchmark: BenchmarkResult, metrics: tuple, lang: str) -> str:
    L = LABELS[lang]
    rows = []
    for column, label_map in metrics:
        for arm_id in benchmark.arms:
            baseline = benchmark.baselines_by_arm[arm_id].metric(column)
            dist = baseline.distribution if baseline else {}
            delta = None
            rel_delta = None
            if benchmark.arm_comparison:
                mc = next((m for m in benchmark.arm_comparison.metrics if m.metric == column), None)
                if mc and arm_id != benchmark.reference_arm_id:
                    delta = mc.deltas.get(f"{arm_id}_vs_{benchmark.reference_arm_id}")
                    ref_mean = mc.group_stats.get(benchmark.reference_arm_id, {}).get("mean")
                    rel_delta = (delta / abs(ref_mean)) if (delta is not None and ref_mean not in (None, 0)) else None
            rows.append(
                [
                    label_map[lang],
                    arm_id,
                    fmt_number(dist.get("mean")),
                    fmt_number(delta) if delta is not None else "—",
                    fmt_signed_percent(rel_delta) if rel_delta is not None else "—",
                    fmt_int(dist.get("count")),
                ]
            )
    return table([L["col_metric"], L["col_arm"], L["col_mean"], L["col_delta"], L["col_relative_delta"], L["col_n"]], rows)


def _render(
    canonical: CanonicalDataset,
    manifest: CampaignManifest,
    benchmark: BenchmarkResult,
    finops: FinOpsReport,
    lang: str,
    logos: dict,
) -> str:
    L = LABELS[lang]

    body = report_header(L["title"], L["subtitle"], lang, logos.get("neomundi_logo"), logos.get("org_name", ""), logos.get("org_logo"))
    body += simulated_notice_block(manifest, lang)
    body += f'<div class="callout">{esc(L["not_a_leaderboard"])}</div>'
    body += f"<p>{esc(L['phrase_under'])}</p>"

    body += f"<h2>{esc(L['s_protocol'])}</h2>" + campaign_meta_grid(manifest, lang)

    body += f"<h2>{esc(L['s_dataset'])}</h2><p>{esc(manifest.dataset_id)} ({esc(manifest.dataset_path)})</p>"

    body += f"<h2>{esc(L['s_models'])}</h2>"
    body += table(
        [L["col_arm"], L["col_n"]],
        [[arm_id, fmt_int(benchmark.baselines_by_arm[arm_id].observation_count)] for arm_id in benchmark.arms],
    )
    body += f'<p><strong>{esc(L["reference_arm"])}:</strong> {esc(benchmark.reference_arm_id or "—")}</p>'

    body += f"<h2>{esc(L['s_runs'])}</h2><p>{fmt_int(manifest.repetitions)}</p>"

    body += f"<h2>{esc(L['s_versions'])}</h2>"
    body += (
        f"<p>{esc(L['col_metric'])}: schema {', '.join(manifest.measurement_schema_versions) or '—'} · "
        f"engine {', '.join(manifest.measurement_engine_versions) or '—'}</p>"
    )

    body += f"<h2>{esc(L['s_behavioural'])}</h2>"
    if benchmark.arm_comparison:
        stability_series = {
            arm: [benchmark.baselines_by_arm[arm].metric("nm_stability_score").distribution.get("mean")]
            for arm in benchmark.arms
        }
        body += grouped_bar_chart(["stability"], stability_series)
    body += _metric_table(benchmark, BEHAVIOURAL_METRICS[:2], lang)

    body += f"<h2>{esc(L['s_stability'])}</h2>"
    least_repeatable = benchmark.repeatability.least_repeatable() if benchmark.repeatability else []
    body += table(
        [L["col_prompt"], L["col_arm"], L["col_stat"], L["col_value"]],
        [[c.prompt_id, c.arm_id, "stdev", fmt_number(c.distribution["stdev"])] for c in least_repeatable],
    )

    body += f"<h2>{esc(L['s_factual'])}</h2>" + _metric_table(benchmark, BEHAVIOURAL_METRICS[2:3], lang)
    body += f"<h2>{esc(L['s_semantic'])}</h2>" + _metric_table(benchmark, BEHAVIOURAL_METRICS[3:5], lang)
    body += f"<h2>{esc(L['s_latency_tokens'])}</h2>" + _metric_table(benchmark, OPERATIONAL_METRICS, lang)

    body += f"<h2>{esc(L['s_density'])}</h2><p><em>{esc(L['s_density_note'])}</em></p>"

    body += f"<h2>{esc(L['s_cost'])}</h2>"
    if finops.estimated_cost:
        body += f"<p>{esc(L['s_cost_note_table'])}</p>"
        body += table(
            [L["col_arm"], L["col_value"]],
            [[arm, fmt_number(cost, 4)] for arm, cost in finops.estimated_cost.items()],
        )
    else:
        body += f"<p>{esc(L['s_cost_note_no_table'])}</p>"

    body += f"<h2>{esc(L['s_prompt_level'])}</h2>"
    prompt_rows = [
        [r["prompt_id"], (r["prompt_text"] or "")[:60], fmt_number(r["spread"])]
        for r in benchmark.prompt_level_variation[:15]
    ]
    body += table([L["col_prompt"], L["col_prompt"], L["col_spread"]], prompt_rows) if prompt_rows else "<p><em>—</em></p>"

    body += f"<h2>{esc(L['s_distribution'])}</h2>"
    dist_rows = []
    for arm_id in benchmark.arms:
        for column, label_map in BEHAVIOURAL_METRICS:
            d = benchmark.baselines_by_arm[arm_id].metric(column).distribution
            dist_rows.append(
                [arm_id, label_map[lang], fmt_number(d.get("mean")), fmt_number(d.get("stdev")), fmt_number(d.get("p05")), fmt_number(d.get("p95"))]
            )
    body += table([L["col_arm"], L["col_metric"], "Mean", "Stdev", "P05", "P95"], dist_rows, max_rows=60)

    body += f"<h2>{esc(L['s_notable'])}</h2>"
    notable = []
    if benchmark.arm_comparison:
        reference = benchmark.arm_comparison.reference_group
        for mc in benchmark.arm_comparison.metrics:
            for arm_id in benchmark.arm_comparison.groups:
                if arm_id == reference:
                    continue
                delta = mc.deltas.get(f"{arm_id}_vs_{reference}")
                if delta is not None:
                    notable.append((abs(delta), mc.label, arm_id, delta))
    notable.sort(key=lambda x: -x[0])
    body += table(
        [L["col_metric"], L["col_arm"], L["col_delta"]],
        [[label, arm_id, fmt_number(delta)] for _, label, arm_id, delta in notable[:10]],
    ) if notable else "<p><em>—</em></p>"

    body += f"<h2>{esc(L['s_limits'])}</h2><ul>" + "".join(f"<li>{esc(item)}</li>" for item in LIMITATIONS[lang]) + "</ul>"

    body += f"<h2>{esc(L['s_manifest'])}</h2>"
    manifest_rows = [[name, sha] for name, sha in manifest.output_files_sha256.items()]
    manifest_rows.append(["campaign_manifest (canonical payload)", manifest.canonical_payload_hash])
    if manifest.dataset_sha256:
        manifest_rows.append([manifest.dataset_path, manifest.dataset_sha256])
    body += table([L["col_file"], L["col_sha256"]], manifest_rows)

    body += boundary_footer(lang, ENGINE_VERSION)
    return html_doc(L["title"], body, lang)


def generate_model_release_benchmark(
    canonical: CanonicalDataset,
    manifest: CampaignManifest,
    output_dir: str | Path,
    lang: str = "en",
    reference_arm_id: str | None = None,
    price_table: PriceTable | None = None,
    organization_name: str = "",
    organization_logo: Path | None = None,
    neomundi_logo: Path | None = None,
    render_pdf: bool = True,
    pdf_engine: str = "auto",
) -> ModelReleaseBenchmarkResult:
    require_language(lang)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    effective_reference_arm = reference_arm_id or manifest.baseline_arm_id
    benchmark = build_benchmark(canonical, reference_arm_id=effective_reference_arm)
    finops = analyze_finops(canonical, price_table=price_table)

    logos = {"neomundi_logo": neomundi_logo, "org_name": organization_name, "org_logo": organization_logo}
    html_content = _render(canonical, manifest, benchmark, finops, lang, logos)

    html_path = output_dir / f"model_release_benchmark_{lang}.html"
    html_path.write_text(html_content, encoding="utf-8")

    pdf_path = None
    pdf_engine_used = None
    if render_pdf:
        candidate = output_dir / f"model_release_benchmark_{lang}.pdf"
        ok, engine = html_to_pdf(html_path, candidate, pdf_engine)
        if ok:
            pdf_path = candidate
            pdf_engine_used = engine

    return ModelReleaseBenchmarkResult(html_path=html_path, pdf_path=pdf_path, pdf_engine=pdf_engine_used)
