"""Minimal, dependency-free HTML composition shared by every open report.

No templating engine: small, explicit functions, in the spirit of the
methodological reference (snapshot.py / the Euria generator's cover/cards/
dataframe_html helpers), generalized so both open reports share one
implementation instead of two copies.
"""

from __future__ import annotations

import base64
import html
import math
from pathlib import Path
from typing import Any


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def safe_float(value: Any) -> float | None:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def fmt_number(value: Any, digits: int = 3) -> str:
    x = safe_float(value)
    return "—" if x is None else f"{x:.{digits}f}"


def fmt_int(value: Any) -> str:
    x = safe_float(value)
    return "—" if x is None else f"{int(round(x)):,}"


def fmt_percent(value: Any, digits: int = 1) -> str:
    x = safe_float(value)
    return "—" if x is None else f"{x * 100:.{digits}f}%"


def fmt_signed_percent(value: Any, digits: int = 1) -> str:
    x = safe_float(value)
    if x is None:
        return "—"
    sign = "+" if x >= 0 else ""
    return f"{sign}{x * 100:.{digits}f}%"


def image_data_uri(path: Path | None) -> str:
    if not path or not path.exists():
        return ""
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
    }.get(path.suffix.lower(), "application/octet-stream")
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def base_css() -> str:
    return r"""
    @page { size:A4; margin:12mm; }
    :root { --ink:#17202a; --muted:#66717d; --line:#dce2e8; --soft:#f5f7f9; --paper:#fff; --accent:#17202a; }
    * { box-sizing:border-box; }
    body { margin:0; background:#eef1f4; color:var(--ink); font-family:Arial,Helvetica,sans-serif; line-height:1.45; }
    main { max-width:960px; margin:0 auto; background:var(--paper); min-height:100vh; }
    .page { padding:16mm 14mm; }
    .brands { display:flex; justify-content:space-between; align-items:center; gap:12mm; padding-bottom:7mm; border-bottom:1px solid var(--line); }
    .brand { display:flex; align-items:center; gap:4mm; min-height:16mm; }
    .brand img { max-height:15mm; max-width:44mm; object-fit:contain; }
    .brand-name { font-weight:700; font-size:10pt; }
    h1 { font-size:23pt; margin:9mm 0 2mm; letter-spacing:-.3px; }
    h2 { font-size:13pt; margin:8mm 0 3mm; }
    h3 { font-size:11pt; margin:5mm 0 2mm; }
    .subtitle { color:var(--muted); font-size:11.5pt; margin-bottom:7mm; }
    .meta { display:grid; grid-template-columns:repeat(2,1fr); gap:3mm 8mm; margin:5mm 0 7mm; font-size:9.5pt; }
    .meta-item { padding:3mm 0; border-bottom:1px solid var(--line); }
    .meta-label { color:var(--muted); font-size:8pt; text-transform:uppercase; letter-spacing:.5px; }
    .meta-value { font-weight:700; overflow-wrap:anywhere; }
    .metric-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:4mm; margin:6mm 0; }
    .metric { border:1px solid var(--line); border-radius:7px; padding:5mm; min-height:24mm; background:#fff; }
    .metric .value { font-size:18pt; font-weight:800; }
    .metric .label { color:var(--muted); font-size:8.5pt; margin-top:1mm; }
    table { width:100%; border-collapse:collapse; font-size:9pt; margin:3mm 0; }
    th, td { text-align:left; padding:2mm 2.5mm; border-bottom:1px solid var(--line); }
    th { color:var(--muted); font-weight:700; font-size:8pt; text-transform:uppercase; letter-spacing:.3px; }
    .callout { background:var(--soft); border-left:4px solid var(--accent); padding:4mm 5mm; margin:4mm 0; font-size:9.5pt; }
    .badge { display:inline-block; padding:.5mm 2mm; border-radius:4px; font-size:8pt; font-weight:700; }
    .badge-high { background:#fde2e1; color:#8a1f1f; }
    .badge-review { background:#fef1cf; color:#7a5b06; }
    .badge-routine { background:#e4f3e6; color:#1f5a2c; }
    .boundary { margin-top:8mm; padding-top:5mm; border-top:1px solid var(--line); color:var(--muted); font-size:8.5pt; }
    .boundary strong { color:var(--ink); }
    .footer { display:flex; justify-content:space-between; gap:5mm; margin-top:8mm; color:var(--muted); font-size:7.8pt; }
    .chart { margin:4mm 0; }
    section.section { margin:6mm 0; }
    @media print { body { background:#fff; } main { max-width:none; } }
    """


def html_doc(title: str, body: str, lang: str = "en") -> str:
    return (
        f'<!doctype html><html lang="{esc(lang)}"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{esc(title)}</title><style>{base_css()}</style></head>"
        f"<body><main><div class=\"page\">{body}</div></main></body></html>"
    )


def brands_block(neomundi_logo: Path | None, org_name: str, org_logo: Path | None) -> str:
    nm_uri = image_data_uri(neomundi_logo)
    org_uri = image_data_uri(org_logo)
    nm = f'<img src="{nm_uri}" alt="NeoMundi">' if nm_uri else '<div class="brand-name">NeoMundi</div>'
    org = (f'<img src="{org_uri}" alt="{esc(org_name or "Organization")}">' if org_uri else "") + (
        f'<div class="brand-name">{esc(org_name)}</div>' if org_name else ""
    )
    if not org:
        org = '<div class="brand-name">Campaign</div>'
    return f'<div class="brands"><div class="brand">{org}</div><div class="brand">{nm}</div></div>'


def metric_cards(items: list[tuple[str, str]]) -> str:
    cells = "".join(f'<div class="metric"><div class="value">{esc(v)}</div><div class="label">{esc(l)}</div></div>' for v, l in items)
    return f'<div class="metric-grid">{cells}</div>'


def meta_grid(items: list[tuple[str, str]]) -> str:
    cells = "".join(
        f'<div class="meta-item"><div class="meta-label">{esc(l)}</div><div class="meta-value">{esc(v)}</div></div>'
        for l, v in items
    )
    return f'<div class="meta">{cells}</div>'


def table(headers: list[str], rows: list[list[Any]], max_rows: int = 40) -> str:
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body_rows = rows[:max_rows]
    body = "".join("<tr>" + "".join(f"<td>{esc(cell)}</td>" for cell in row) + "</tr>" for row in body_rows)
    note = f'<p style="color:var(--muted);font-size:8pt;">Showing {len(body_rows)} of {len(rows)} rows.</p>' if len(rows) > max_rows else ""
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>{note}"


def badge(priority: str) -> str:
    css_class = {"HIGH_REVIEW": "badge-high", "REVIEW": "badge-review", "ROUTINE": "badge-routine"}.get(priority, "badge-routine")
    return f'<span class="badge {css_class}">{esc(priority)}</span>'


def section(title: str, body_html: str) -> str:
    return f'<section class="section"><h2>{esc(title)}</h2>{body_html}</section>'
