"""HTML -> PDF, with a Playwright-first / WeasyPrint-fallback strategy.

Both are optional dependencies. If neither is installed, report generation
still succeeds for HTML; PDF is skipped with a clear message rather than a
hard failure.
"""

from __future__ import annotations

from pathlib import Path


def html_to_pdf(html_path: Path, pdf_path: Path, engine: str = "auto") -> tuple[bool, str]:
    errors = []

    if engine in ("auto", "playwright"):
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
                page.pdf(
                    path=str(pdf_path),
                    format="A4",
                    print_background=True,
                    prefer_css_page_size=True,
                    margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"},
                )
                browser.close()
            return True, "playwright"
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Playwright: {exc}")
            if engine == "playwright":
                return False, " | ".join(errors)

    if engine in ("auto", "weasyprint"):
        try:
            from weasyprint import HTML

            HTML(filename=str(html_path)).write_pdf(str(pdf_path))
            return True, "weasyprint"
        except Exception as exc:  # noqa: BLE001
            errors.append(f"WeasyPrint: {exc}")

    return False, " | ".join(errors) if errors else "no PDF engine available"
