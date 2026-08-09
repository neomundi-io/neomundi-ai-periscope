#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""NeoMundi AI Periscope — Campaign Snapshot v0.1.0

Generate a lightweight co-branded HTML + PDF snapshot from an AI Periscope
campaign result file (.json, .jsonl or .csv).

Measured signal, not a verdict.
"""

from __future__ import annotations

import argparse
import base64
import csv
import html
import json
import math
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("Install PyYAML: python -m pip install PyYAML") from exc

VERSION = "0.1.0"

ALIASES = {
    "stability": ["stability_score", "stability", "g_final", "g_score", "g"],
    "delta_g": ["delta_g", "deltaG", "dg", "delta_g_score", "g_delta"],
    "decision": ["decision", "observation_class", "status", "classification"],
    "latency_ms": ["latency_ms", "latency", "response_latency_ms", "duration_ms"],
    "token_count": ["token_count", "tokens", "total_tokens", "output_tokens"],
    "error": ["error", "error_message", "exception"],
    "prompt": ["prompt", "input", "question", "user_prompt"],
    "prompt_id": ["prompt_id", "question_id", "input_id"],
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate an AI Periscope Campaign Snapshot.")
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--config", type=Path, default=Path("config.yaml"))
    p.add_argument("--output-dir", type=Path, default=None)
    p.add_argument("--neomundi-logo", type=Path, default=Path("assets/LOGO_NeoMundi_Controltower.png"))
    p.add_argument("--organization-name", default="")
    p.add_argument("--organization-logo", type=Path, default=None)
    p.add_argument("--language", choices=["fr", "en"], default="en")
    p.add_argument("--pdf-engine", choices=["auto", "playwright", "weasyprint"], default="auto")
    p.add_argument("--no-pdf", action="store_true")
    return p.parse_args()


def esc(v: Any) -> str:
    return html.escape("" if v is None else str(v))


def safe_float(v: Any) -> float | None:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def fmt_number(v: Any, digits: int = 3) -> str:
    x = safe_float(v)
    return "—" if x is None else f"{x:.{digits}f}"


def fmt_int(v: Any) -> str:
    x = safe_float(v)
    return "—" if x is None else f"{int(round(x)):,}"


def fmt_percent(v: Any, digits: int = 1) -> str:
    x = safe_float(v)
    return "—" if x is None else f"{x * 100:.{digits}f}%"


def image_data_uri(path: Path | None) -> str:
    if not path or not path.exists():
        return ""
    mime = {".png":"image/png", ".jpg":"image/jpeg", ".jpeg":"image/jpeg", ".webp":"image/webp", ".svg":"image/svg+xml"}.get(path.suffix.lower(), "application/octet-stream")
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def load_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    s = path.suffix.lower()
    if s == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            rows = data
        elif isinstance(data, dict):
            rows = next((data[k] for k in ("results", "observations", "rows", "data") if isinstance(data.get(k), list)), [data])
        else:
            raise ValueError("Unsupported JSON structure")
    elif s == ".jsonl":
        rows = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    obj = json.loads(line)
                    if isinstance(obj, dict):
                        rows.append(obj)
    elif s == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
    else:
        raise ValueError("Supported input formats: .json, .jsonl, .csv")
    rows = [r for r in rows if isinstance(r, dict)]
    if not rows:
        raise ValueError("No observations found")
    return rows


def first_present(row: dict[str, Any], names: list[str]) -> Any:
    for k in names:
        if k in row and row[k] not in (None, ""):
            return row[k]
    return None


def numeric_values(rows: list[dict[str, Any]], key: str) -> list[float]:
    out = []
    for row in rows:
        x = safe_float(first_present(row, ALIASES[key]))
        if x is not None:
            out.append(x)
    return out


def mean(values: list[float]) -> float | None:
    return statistics.fmean(values) if values else None


def flag_rate(rows: list[dict[str, Any]]) -> float | None:
    vals = []
    for row in rows:
        raw = first_present(row, ALIASES["decision"])
        if raw is not None:
            vals.append(str(raw).strip().upper())
    if not vals:
        return None
    n = sum(1 for v in vals if v == "FLAG" or "FLAGGED" in v or v == "HIGH_REVIEW")
    return n / len(vals)


def error_count(rows: list[dict[str, Any]]) -> int:
    n = 0
    for row in rows:
        raw = first_present(row, ALIASES["error"])
        if raw not in (None, "", False, 0, "0", "None", "null"):
            n += 1
    return n


def prompt_key(row: dict[str, Any], i: int) -> str:
    pid = first_present(row, ALIASES["prompt_id"])
    if pid not in (None, ""):
        return str(pid)
    p = first_present(row, ALIASES["prompt"])
    if p not in (None, ""):
        t = str(p).strip().replace("\n", " ")
        return t[:72] + ("…" if len(t) > 72 else "")
    return f"Prompt {i}"


def most_variable_prompt(rows: list[dict[str, Any]]) -> tuple[str, float | None]:
    groups: dict[str, list[float]] = {}
    for i, row in enumerate(rows, start=1):
        x = safe_float(first_present(row, ALIASES["stability"]))
        if x is not None:
            groups.setdefault(prompt_key(row, i), []).append(x)
    best_name, best_spread = "—", None
    for name, vals in groups.items():
        if len(vals) < 2:
            continue
        spread = max(vals) - min(vals)
        if best_spread is None or spread > best_spread:
            best_name, best_spread = name, spread
    return best_name, best_spread


def labels(lang: str) -> dict[str, str]:
    if lang == "fr":
        return {
            "title":"AI Periscope — Snapshot de campagne",
            "subtitle":"Synthèse légère de la campagne et des principaux signaux de mesure runtime.",
            "organization":"Organisation", "provider":"Provider", "model":"Modèle",
            "prompt_file":"Fichier de prompts", "generated":"Généré", "coverage":"Couverture",
            "observations":"Observations", "stability":"Stabilité moyenne", "dg":"ΔG moyen",
            "flag":"Taux FLAG", "latency":"Latence moyenne (ms)", "tokens":"Tokens moyens",
            "variable":"Prompt le plus variable", "spread":"Plus forte amplitude de stabilité entre répétitions :",
            "scope":"Frontière d’interprétation",
            "scope_text":"Ce document résume des signaux observés pendant cette campagne. Il ne constitue ni un verdict factuel, ni une certification de sécurité, ni une conclusion réglementaire. Les résultats valent pour le provider, le modèle, le corpus, les paramètres et la période documentés.",
            "boundary":"Signal mesuré, pas verdict.", "through":"Mesuré via NeoMundi ControlTower",
        }
    return {
        "title":"AI Periscope — Campaign Snapshot",
        "subtitle":"Lightweight summary of the campaign and selected runtime measurement signals.",
        "organization":"Organization", "provider":"Provider", "model":"Model",
        "prompt_file":"Prompt file", "generated":"Generated", "coverage":"Coverage",
        "observations":"Observations", "stability":"Mean stability", "dg":"Mean ΔG",
        "flag":"FLAG rate", "latency":"Mean latency (ms)", "tokens":"Mean tokens",
        "variable":"Most variable prompt", "spread":"Largest observed stability range across repetitions:",
        "scope":"Interpretation boundary",
        "scope_text":"This document summarizes signals observed during this campaign. It is not a factual verdict, a safety certification, or a regulatory conclusion. Results apply only to the documented provider, model, corpus, parameters, and period.",
        "boundary":"Measured signal, not a verdict.", "through":"Measured through NeoMundi ControlTower",
    }


def css() -> str:
    return r"""
    @page { size:A4; margin:12mm; }
    :root { --ink:#17202a; --muted:#66717d; --line:#dce2e8; --soft:#f5f7f9; --paper:#fff; }
    * { box-sizing:border-box; }
    body { margin:0; background:#eef1f4; color:var(--ink); font-family:Arial,Helvetica,sans-serif; line-height:1.45; }
    main { max-width:900px; margin:0 auto; background:var(--paper); min-height:100vh; }
    .page { padding:16mm 14mm; }
    .brands { display:flex; justify-content:space-between; align-items:center; gap:12mm; padding-bottom:7mm; border-bottom:1px solid var(--line); }
    .brand { display:flex; align-items:center; gap:4mm; min-height:18mm; }
    .brand img { max-height:17mm; max-width:44mm; object-fit:contain; }
    .brand-name { font-weight:700; font-size:10pt; }
    h1 { font-size:25pt; margin:10mm 0 2mm; letter-spacing:-.4px; }
    .subtitle { color:var(--muted); font-size:12pt; margin-bottom:8mm; }
    .meta { display:grid; grid-template-columns:repeat(2,1fr); gap:3mm 8mm; margin:5mm 0 8mm; font-size:9.5pt; }
    .meta-item { padding:3mm 0; border-bottom:1px solid var(--line); }
    .meta-label { color:var(--muted); font-size:8pt; text-transform:uppercase; letter-spacing:.5px; }
    .meta-value { font-weight:700; overflow-wrap:anywhere; }
    .metric-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:4mm; margin:6mm 0; }
    .metric { border:1px solid var(--line); border-radius:7px; padding:5mm; min-height:26mm; background:#fff; }
    .value { font-size:19pt; font-weight:800; }
    .label { color:var(--muted); font-size:8.5pt; margin-top:1mm; }
    h2 { font-size:13pt; margin:8mm 0 3mm; }
    .callout { background:var(--soft); border-left:4px solid #111; padding:4mm 5mm; margin:4mm 0; font-size:9.5pt; }
    .boundary { margin-top:8mm; padding-top:5mm; border-top:1px solid var(--line); color:var(--muted); font-size:8.5pt; }
    .boundary strong { color:var(--ink); }
    .footer { display:flex; justify-content:space-between; gap:5mm; margin-top:8mm; color:var(--muted); font-size:7.8pt; }
    @media print { body { background:#fff; } main { max-width:none; } }
    """


def metric_cards(items: list[tuple[str,str]]) -> str:
    return '<div class="metric-grid">' + ''.join(f'<div class="metric"><div class="value">{esc(v)}</div><div class="label">{esc(l)}</div></div>' for v,l in items) + '</div>'


def render(rows: list[dict[str,Any]], config: dict[str,Any], org_name: str, nm_logo: Path|None, org_logo: Path|None, lang: str) -> str:
    t = labels(lang)
    stability = numeric_values(rows, "stability")
    dg = numeric_values(rows, "delta_g")
    latency = numeric_values(rows, "latency_ms")
    tokens = numeric_values(rows, "token_count")
    errors = error_count(rows)
    total = len(rows)
    coverage = (total - errors) / total if total else None
    variable_name, spread = most_variable_prompt(rows)
    nm_uri, org_uri = image_data_uri(nm_logo), image_data_uri(org_logo)
    nm = f'<img src="{nm_uri}" alt="NeoMundi">' if nm_uri else '<div class="brand-name">NeoMundi</div>'
    org = (f'<img src="{org_uri}" alt="{esc(org_name or "Organization")}">' if org_uri else '') + (f'<div class="brand-name">{esc(org_name)}</div>' if org_name else '')
    if not org:
        org = '<div class="brand-name">Campaign</div>'
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    cards = metric_cards([
        (fmt_int(total), t["observations"]),
        (fmt_number(mean(stability),3), t["stability"]),
        (fmt_number(mean(dg),3), t["dg"]),
        (fmt_percent(flag_rate(rows),1), t["flag"]),
        (fmt_number(mean(latency),1), t["latency"]),
        (fmt_number(mean(tokens),1), t["tokens"]),
    ])
    return f'''<!doctype html><html lang="{esc(lang)}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(t["title"])}</title><style>{css()}</style></head><body><main><div class="page">
    <div class="brands"><div class="brand">{org}</div><div class="brand">{nm}</div></div>
    <h1>{esc(t["title"])}</h1><div class="subtitle">{esc(t["subtitle"])}</div>
    <div class="meta">
      <div class="meta-item"><div class="meta-label">{esc(t["organization"])}</div><div class="meta-value">{esc(org_name or "—")}</div></div>
      <div class="meta-item"><div class="meta-label">{esc(t["provider"])}</div><div class="meta-value">{esc(config.get("provider","—"))}</div></div>
      <div class="meta-item"><div class="meta-label">{esc(t["model"])}</div><div class="meta-value">{esc(config.get("model","—"))}</div></div>
      <div class="meta-item"><div class="meta-label">{esc(t["prompt_file"])}</div><div class="meta-value">{esc(config.get("prompt_file","—"))}</div></div>
      <div class="meta-item"><div class="meta-label">{esc(t["generated"])}</div><div class="meta-value">{esc(generated)}</div></div>
      <div class="meta-item"><div class="meta-label">{esc(t["coverage"])}</div><div class="meta-value">{esc(fmt_percent(coverage,1))}</div></div>
    </div>
    {cards}
    <h2>{esc(t["variable"])}</h2><div class="callout"><strong>{esc(variable_name)}</strong><br>{esc(t["spread"])} {esc(fmt_number(spread,3))}</div>
    <h2>{esc(t["scope"])}</h2><div class="callout">{esc(t["scope_text"])}</div>
    <div class="boundary"><strong>{esc(t["boundary"])}</strong><br>{esc(t["through"])} · AI Periscope v{VERSION}</div>
    <div class="footer"><div>NeoMundi Research</div><div>{esc(generated)}</div></div>
    </div></main></body></html>'''


def html_to_pdf(html_path: Path, pdf_path: Path, engine: str) -> tuple[bool,str]:
    errors = []
    if engine in ("auto","playwright"):
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
                page.pdf(path=str(pdf_path), format="A4", print_background=True, prefer_css_page_size=True, margin={"top":"0mm","right":"0mm","bottom":"0mm","left":"0mm"})
                browser.close()
            return True, "playwright"
        except Exception as exc:
            errors.append(f"Playwright: {exc}")
            if engine == "playwright":
                return False, " | ".join(errors)
    if engine in ("auto","weasyprint"):
        try:
            from weasyprint import HTML
            HTML(filename=str(html_path)).write_pdf(str(pdf_path))
            return True, "weasyprint"
        except Exception as exc:
            errors.append(f"WeasyPrint: {exc}")
    return False, " | ".join(errors)


def main() -> int:
    args = parse_args()
    input_path = args.input.expanduser().resolve()
    config_path = args.config.expanduser().resolve()
    rows = load_rows(input_path)
    config = load_config(config_path)
    output = args.output_dir.expanduser().resolve() if args.output_dir else input_path.parent
    output.mkdir(parents=True, exist_ok=True)
    html_path = output / "AI_PERISCOPE_SNAPSHOT.html"
    pdf_path = output / "AI_PERISCOPE_SNAPSHOT.pdf"
    html_doc = render(
        rows, config, args.organization_name,
        args.neomundi_logo.expanduser().resolve() if args.neomundi_logo else None,
        args.organization_logo.expanduser().resolve() if args.organization_logo else None,
        args.language,
    )
    html_path.write_text(html_doc, encoding="utf-8")
    print(f"HTML snapshot: {html_path}")
    if args.no_pdf:
        print("PDF skipped (--no-pdf).")
        return 0
    ok, detail = html_to_pdf(html_path, pdf_path, args.pdf_engine)
    if ok:
        print(f"PDF snapshot : {pdf_path}")
        print(f"PDF engine   : {detail}")
    else:
        print("PDF could not be generated; HTML remains available.")
        print(f"Details: {detail}")
        print("Optional: python -m pip install playwright weasyprint")
        print("Then:     python -m playwright install chromium")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
