"""Dependency-free inline SVG charts.

The methodological reference (Euria generator) rasters charts with
matplotlib to PNG. The open reports intentionally avoid that dependency:
inline SVG keeps HTML output self-contained, deterministic (easy to assert
on in tests), and rendering-engine-agnostic for the PDF export step.
"""

from __future__ import annotations

from periscope.reports.common.html import esc


def grouped_bar_chart(
    group_labels: list[str],
    series: dict[str, list[float | None]],
    width: int = 760,
    height: int = 280,
    value_format: str = "{:.2f}",
) -> str:
    """`series` maps a series name (e.g. an arm_id) to one value per group_label."""
    if not group_labels or not series:
        return '<div class="chart"><em>No data to chart.</em></div>'

    margin_left, margin_bottom, margin_top = 44, 60, 16
    plot_w = width - margin_left - 16
    plot_h = height - margin_bottom - margin_top

    all_values = [v for values in series.values() for v in values if v is not None]
    if not all_values:
        return '<div class="chart"><em>No measured values to chart.</em></div>'
    v_min = min(0.0, min(all_values))
    v_max = max(all_values) if max(all_values) > 0 else 1.0
    span = (v_max - v_min) or 1.0

    def y_of(value: float) -> float:
        return margin_top + plot_h - ((value - v_min) / span) * plot_h

    zero_y = y_of(0.0)

    series_names = list(series.keys())
    n_series = len(series_names)
    group_w = plot_w / max(1, len(group_labels))
    bar_w = max(4.0, (group_w * 0.7) / max(1, n_series))
    palette = ["#17202a", "#5b7a99", "#a7c4d9", "#c98a3d", "#8a1f1f", "#1f5a2c"]

    bars = []
    for gi, label in enumerate(group_labels):
        group_x0 = margin_left + gi * group_w + group_w * 0.15
        for si, name in enumerate(series_names):
            value = series[name][gi] if gi < len(series[name]) else None
            x = group_x0 + si * bar_w
            color = palette[si % len(palette)]
            if value is None:
                bars.append(
                    f'<text x="{x + bar_w/2:.1f}" y="{zero_y - 4:.1f}" font-size="7" text-anchor="middle" fill="#999">n/a</text>'
                )
                continue
            y = y_of(value)
            bar_top = min(y, zero_y)
            bar_h = abs(zero_y - y)
            bars.append(
                f'<rect x="{x:.1f}" y="{bar_top:.1f}" width="{bar_w - 1.5:.1f}" height="{max(bar_h,0.5):.1f}" fill="{color}"/>'
            )

    x_labels = []
    for gi, label in enumerate(group_labels):
        x = margin_left + gi * group_w + group_w / 2
        x_labels.append(
            f'<text x="{x:.1f}" y="{height - margin_bottom + 16:.1f}" font-size="8" text-anchor="middle" fill="#66717d">{esc(label)}</text>'
        )

    legend = []
    for si, name in enumerate(series_names):
        lx = margin_left + si * 130
        ly = height - 14
        legend.append(
            f'<rect x="{lx:.1f}" y="{ly-8:.1f}" width="8" height="8" fill="{palette[si % len(palette)]}"/>'
            f'<text x="{lx+12:.1f}" y="{ly-1:.1f}" font-size="7.5" fill="#17202a">{esc(name)}</text>'
        )

    axis = f'<line x1="{margin_left}" y1="{zero_y:.1f}" x2="{width-16}" y2="{zero_y:.1f}" stroke="#dce2e8" stroke-width="1"/>'

    svg = (
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" role="img" '
        f'xmlns="http://www.w3.org/2000/svg">'
        f'{axis}{"".join(bars)}{"".join(x_labels)}{"".join(legend)}</svg>'
    )
    return f'<div class="chart">{svg}</div>'


def sparkline(values: list[float | None], width: int = 320, height: int = 60) -> str:
    usable = [(i, v) for i, v in enumerate(values) if v is not None]
    if len(usable) < 2:
        return '<div class="chart"><em>Not enough points to chart.</em></div>'

    xs = [i for i, _ in usable]
    ys = [v for _, v in usable]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    x_span = (x_max - x_min) or 1
    y_span = (y_max - y_min) or 1

    def point(i: int, v: float) -> tuple[float, float]:
        x = 8 + (i - x_min) / x_span * (width - 16)
        y = height - 8 - (v - y_min) / y_span * (height - 16)
        return x, y

    points = " ".join(f"{x:.1f},{y:.1f}" for x, y in (point(i, v) for i, v in usable))
    svg = (
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" role="img" '
        f'xmlns="http://www.w3.org/2000/svg">'
        f'<polyline points="{points}" fill="none" stroke="#17202a" stroke-width="2"/>'
        f"</svg>"
    )
    return f'<div class="chart">{svg}</div>'
