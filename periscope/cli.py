"""AI Periscope CLI.

    periscope run campaign.yaml [--simulate]
    periscope report <campaign_dir_or_id> --type snapshot
    periscope report <campaign_dir_or_id> --type model-release-benchmark

Only the two public report types are wired into the CLI in this build.
Everything under periscope/analysis/ is reachable programmatically for
advanced/custom reporting -- see periscope/reports/advanced/README.md.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from periscope import __version__
from periscope.campaign.runner import run_campaign
from periscope.export.json_export import load_canonical_json
from periscope.export.manifest import load_manifest
from periscope.measurement.client import NeoMundiControlTowerClient
from periscope.measurement.simulated import SimulatedMeasurementClient
from periscope.reports.open.executive_snapshot import generate_executive_snapshot
from periscope.reports.open.model_release_benchmark import generate_model_release_benchmark


def _resolve_campaign_dir(value: str, default_output_dir: str) -> Path:
    as_path = Path(value)
    if as_path.exists() and (as_path / "campaign_manifest.json").exists():
        return as_path
    candidate = Path(default_output_dir) / value
    if (candidate / "campaign_manifest.json").exists():
        return candidate
    raise SystemExit(f"Could not find a campaign at {value!r} (looked in {as_path} and {candidate}).")


def _cmd_run(args: argparse.Namespace) -> int:
    if args.simulate:
        client = SimulatedMeasurementClient(partial_rate=args.simulate_partial_rate, flag_rate=args.simulate_flag_rate)
    else:
        api_key = args.neomundi_api_key or os.getenv("NEOMUNDI_API_KEY")
        if not api_key:
            raise SystemExit(
                "Missing NeoMundi API key. Set NEOMUNDI_API_KEY or pass --neomundi-api-key, "
                "or use --simulate for an offline demo campaign."
            )
        client = NeoMundiControlTowerClient(neomundi_api_key=api_key, base_url=args.base_url)

    def progress(index: int, total: int, observation) -> None:
        status = "ERROR" if observation.error else (observation.measurement.decision if observation.measurement else "?")
        print(f"[{index}/{total}] {observation.prompt_id} / {observation.arm_id} / rep {observation.repetition_index} -> {status}")

    result = run_campaign(args.campaign_file, client=client, simulated=args.simulate, progress_callback=progress)

    print("")
    print("Campaign complete.")
    print(f"Campaign ID     : {result.config.campaign_id}")
    print(f"Observations    : {result.canonical_dataset.observation_count}")
    print(f"Errors          : {result.canonical_dataset.error_count}")
    print(f"Output          : {result.output_dir}")
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    campaign_dir = _resolve_campaign_dir(args.campaign, args.output_dir)
    canonical = load_canonical_json(campaign_dir / "campaign_results.json")
    manifest = load_manifest(campaign_dir / "campaign_manifest.json")

    languages = ["fr", "en"] if args.lang == "both" else [args.lang]
    org_logo = Path(args.org_logo) if args.org_logo else None
    neomundi_logo = Path(args.neomundi_logo) if args.neomundi_logo else None

    for lang in languages:
        if args.type == "snapshot":
            result = generate_executive_snapshot(
                canonical,
                manifest,
                output_dir=campaign_dir / "reports",
                lang=lang,
                organization_name=args.org_name,
                organization_logo=org_logo,
                neomundi_logo=neomundi_logo,
                render_pdf=not args.no_pdf,
            )
        elif args.type == "model-release-benchmark":
            result = generate_model_release_benchmark(
                canonical,
                manifest,
                output_dir=campaign_dir / "reports",
                lang=lang,
                reference_arm_id=args.reference_arm,
                organization_name=args.org_name,
                organization_logo=org_logo,
                neomundi_logo=neomundi_logo,
                render_pdf=not args.no_pdf,
            )
        else:
            raise SystemExit(f"Unknown report type: {args.type!r}")

        print(f"[{lang}] HTML: {result.html_path}")
        if result.pdf_path:
            print(f"[{lang}] PDF : {result.pdf_path} ({result.pdf_engine})")
        else:
            print(f"[{lang}] PDF : not generated")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="periscope", description="NeoMundi AI Periscope Layer")
    parser.add_argument("--version", action="version", version=f"periscope {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a campaign from a campaign.yaml file.")
    run_parser.add_argument("campaign_file")
    run_parser.add_argument("--simulate", action="store_true", help="Use the offline simulator instead of live NeoMundi/provider calls.")
    run_parser.add_argument("--simulate-partial-rate", type=float, default=0.0)
    run_parser.add_argument("--simulate-flag-rate", type=float, default=0.1)
    run_parser.add_argument("--neomundi-api-key", default=None)
    run_parser.add_argument("--base-url", default="https://api.neomundi.io")
    run_parser.set_defaults(func=_cmd_run)

    report_parser = subparsers.add_parser("report", help="Generate a report from a completed campaign.")
    report_parser.add_argument("campaign", help="Campaign directory, or campaign_id under --output-dir.")
    report_parser.add_argument("--type", choices=["snapshot", "model-release-benchmark"], required=True)
    report_parser.add_argument("--lang", choices=["fr", "en", "both"], default="en")
    report_parser.add_argument("--output-dir", default="examples/outputs")
    report_parser.add_argument("--reference-arm", default=None, help="Arm ID to compare against (model-release-benchmark only).")
    report_parser.add_argument("--org-name", default="")
    report_parser.add_argument("--org-logo", default=None)
    report_parser.add_argument("--neomundi-logo", default="assets/LOGO_NeoMundi_Controltower.png")
    report_parser.add_argument("--no-pdf", action="store_true")
    report_parser.set_defaults(func=_cmd_report)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
