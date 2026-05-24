"""CLI for DUAT predictive registry utilities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .benchmark_matrix import (
    RUN_ID_V0_4,
    run_benchmark_matrix,
    write_license_comparability_markdown,
    write_matrix_json,
    write_matrix_markdown,
)
from .benchmarking import run_benchmark
from .domain_calibration import (
    calibrate_matrix,
    write_domain_calibration_json,
    write_domain_calibration_markdown,
)
from .domain_weight_calibration import (
    calibrate_domain_weights,
    write_domain_weight_json,
    write_domain_weight_markdown,
)
from .metric_aligned_r import (
    build_metric_aligned_report,
    write_metric_aligned_json,
    write_metric_aligned_markdown,
)
from .nested_backtest import (
    run_nested_domain_backtest,
    write_nested_backtest_json,
    write_nested_backtest_markdown,
)
from .objectives import find_workspace_root, resolve_workspace_path
from .reporting import write_json_report, write_markdown_report
from data_readiness.official_series_manifest import load_manifest
from data_readiness.readiness_rules import (
    evaluate_manifest_readiness,
    write_readiness_json,
    write_readiness_markdown,
)
from data_readiness.world_bank_wdi_validate import (
    build_wdi_source_pack_report,
    run_wdi_source_pack,
    validate_wdi_manifest,
    write_wdi_report,
)
from data_readiness.world_bank_wdi_governance_review import (
    run_wdi_governance_review,
    write_governance_json,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="duat_predictive_registry")
    subparsers = parser.add_subparsers(dest="command", required=True)

    benchmark = subparsers.add_parser("benchmark", help="Run offline R_before/R_after benchmark")
    benchmark.add_argument("--objective", required=True, help="Predictive objective JSON")
    benchmark.add_argument("--out", required=True, help="Output JSON report path")
    benchmark.add_argument("--markdown-out", help="Optional Markdown report path")
    benchmark.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    matrix = subparsers.add_parser("benchmark-matrix", help="Run offline benchmark matrix")
    matrix.add_argument("--objectives", nargs="+", required=True, help="Predictive objective JSON files")
    matrix.add_argument("--out", required=True, help="Output JSON matrix path")
    matrix.add_argument("--markdown-out", help="Optional Markdown matrix path")
    matrix.add_argument("--review-out", help="Optional license/comparability Markdown path")
    matrix.add_argument("--matrix-version", choices=["v0.3", "v0.4"], help="Optional matrix version override")
    matrix.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    calibrate = subparsers.add_parser("calibrate-domains", help="Run DomainCalibrationGate over a benchmark matrix")
    calibrate.add_argument("--matrix", required=True, help="Benchmark matrix JSON path")
    calibrate.add_argument("--out", required=True, help="Output JSON calibration report path")
    calibrate.add_argument("--markdown-out", help="Optional Markdown calibration report path")
    calibrate.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    metric_align = subparsers.add_parser("metric-align-r", help="Run MetricAlignedR over v0.4 calibration outputs")
    metric_align.add_argument("--calibration", required=True, help="Domain calibration JSON path")
    metric_align.add_argument("--matrix", required=True, help="Benchmark matrix JSON path")
    metric_align.add_argument("--out", required=True, help="Output JSON metric-aligned report path")
    metric_align.add_argument("--markdown-out", help="Optional Markdown metric-aligned report path")
    metric_align.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    domain_weights = subparsers.add_parser("calibrate-domain-weights", help="Run local domain weight calibration diagnostic")
    domain_weights.add_argument("--matrix", required=True, help="Benchmark matrix JSON path")
    domain_weights.add_argument("--out", required=True, help="Output JSON domain weight report path")
    domain_weights.add_argument("--markdown-out", help="Optional Markdown domain weight report path")
    domain_weights.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    nested = subparsers.add_parser("nested-backtest", help="Run nested walk-forward domain backtest")
    nested.add_argument("--matrix", required=True, help="Benchmark matrix v0.4 JSON path")
    nested.add_argument("--metric-aligned", required=True, help="Metric-aligned v0.5 JSON path")
    nested.add_argument("--out", required=True, help="Output JSON nested backtest report path")
    nested.add_argument("--markdown-out", help="Optional Markdown nested backtest report path")
    nested.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    data_readiness = subparsers.add_parser("data-readiness", help="Evaluate official long-history data readiness")
    data_readiness.add_argument("--manifest", required=True, help="Official series manifest JSON path")
    data_readiness.add_argument("--schema", required=True, help="Readiness report schema JSON path")
    data_readiness.add_argument("--out", required=True, help="Output JSON readiness report path")
    data_readiness.add_argument("--markdown-out", help="Optional Markdown readiness report path")
    data_readiness.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    wdi_source_pack = subparsers.add_parser("wdi-source-pack", help="Create World Bank WDI official source pack")
    wdi_source_pack.add_argument("--country", help="World Bank country code. If omitted, detect from existing manifests.")
    wdi_source_pack.add_argument("--indicators", nargs="+", required=True, help="WDI indicator codes")
    wdi_source_pack.add_argument("--out", required=True, help="Output JSON source pack report path")
    wdi_source_pack.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    wdi_governance = subparsers.add_parser("wdi-governance-review", help="Review WDI license/comparability gates")
    wdi_governance.add_argument("--manifest", required=True, help="World Bank WDI v0.8 manifest path")
    wdi_governance.add_argument("--out", required=True, help="Output JSON governance review path")
    wdi_governance.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    wdi_governance.add_argument("--no-external-verify", action="store_true", help="Skip live official terms/metadata verification")

    args = parser.parse_args(argv)
    if args.command == "benchmark":
        root = find_workspace_root(Path.cwd())
        objective_path = _resolve_cli_path(args.objective, root, must_exist=True)
        out_path = _resolve_cli_path(args.out, root, must_exist=False)
        report = run_benchmark(objective_path, root)
        digest = write_json_report(report, out_path, pretty=args.pretty)
        if args.markdown_out:
            write_markdown_report(report, _resolve_cli_path(args.markdown_out, root, must_exist=False))
        print(
            json.dumps(
                {
                    "status": report.get("forecast_gate"),
                    "publication_gate": report.get("publication_gate"),
                    "out": _display_path(out_path, root),
                    "sha256": digest,
                },
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        return 0 if report.get("forecast_gate") != "BLOCK" else 2
    if args.command == "benchmark-matrix":
        root = find_workspace_root(Path.cwd())
        objective_paths = [_resolve_cli_path(path, root, must_exist=True) for path in args.objectives]
        out_path = _resolve_cli_path(args.out, root, must_exist=False)
        matrix_version = args.matrix_version or ("v0.4" if "v0-4" in str(out_path).lower() or "v0_4" in str(out_path).lower() else "v0.3")
        if matrix_version == "v0.4":
            matrix_report = run_benchmark_matrix(objective_paths, root, run_id=RUN_ID_V0_4, schema="duat.benchmark_matrix.v0_4")
        else:
            matrix_report = run_benchmark_matrix(objective_paths, root)
        digest = write_matrix_json(matrix_report, out_path, pretty=args.pretty)
        if args.markdown_out:
            write_matrix_markdown(matrix_report, _resolve_cli_path(args.markdown_out, root, must_exist=False))
        if args.review_out:
            write_license_comparability_markdown(matrix_report, _resolve_cli_path(args.review_out, root, must_exist=False))
        print(
            json.dumps(
                {
                    "status": matrix_report.get("action_gate_local"),
                    "replication_status": matrix_report.get("matrix_interpretation", {}).get("replication_status"),
                    "publication_gate": matrix_report.get("publication_gate"),
                    "out": _display_path(out_path, root),
                    "sha256": digest,
                },
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        return 0 if matrix_report.get("action_gate_local") != "BLOCK" else 2
    if args.command == "calibrate-domains":
        root = find_workspace_root(Path.cwd())
        matrix_path = _resolve_cli_path(args.matrix, root, must_exist=True)
        out_path = _resolve_cli_path(args.out, root, must_exist=False)
        matrix_report = json.loads(matrix_path.read_text(encoding="utf-8"))
        calibration_report = calibrate_matrix(matrix_report, root)
        digest = write_domain_calibration_json(calibration_report, out_path, pretty=args.pretty)
        if args.markdown_out:
            write_domain_calibration_markdown(calibration_report, _resolve_cli_path(args.markdown_out, root, must_exist=False))
        print(
            json.dumps(
                {
                    "status": calibration_report.get("action_gate_local"),
                    "publication_gate": calibration_report.get("publication_gate"),
                    "out": _display_path(out_path, root),
                    "sha256": digest,
                },
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        return 0 if calibration_report.get("action_gate_local") != "BLOCK" else 2
    if args.command == "metric-align-r":
        root = find_workspace_root(Path.cwd())
        calibration_path = _resolve_cli_path(args.calibration, root, must_exist=True)
        matrix_path = _resolve_cli_path(args.matrix, root, must_exist=True)
        out_path = _resolve_cli_path(args.out, root, must_exist=False)
        calibration_report = json.loads(calibration_path.read_text(encoding="utf-8"))
        matrix_report = json.loads(matrix_path.read_text(encoding="utf-8"))
        aligned_report = build_metric_aligned_report(calibration_report, matrix_report)
        payload_sha256, file_sha256 = write_metric_aligned_json(aligned_report, out_path, pretty=args.pretty)
        if args.markdown_out:
            write_metric_aligned_markdown(aligned_report, _resolve_cli_path(args.markdown_out, root, must_exist=False))
        print(
            json.dumps(
                {
                    "status": aligned_report.get("action_gate_local"),
                    "publication_gate": aligned_report.get("publication_gate"),
                    "out": _display_path(out_path, root),
                    "sha256": payload_sha256,
                    "file_sha256": file_sha256,
                },
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        return 0 if aligned_report.get("action_gate_local") != "BLOCK" else 2
    if args.command == "calibrate-domain-weights":
        root = find_workspace_root(Path.cwd())
        matrix_path = _resolve_cli_path(args.matrix, root, must_exist=True)
        out_path = _resolve_cli_path(args.out, root, must_exist=False)
        matrix_report = json.loads(matrix_path.read_text(encoding="utf-8"))
        weight_report = calibrate_domain_weights(matrix_report)
        payload_sha256, file_sha256 = write_domain_weight_json(weight_report, out_path, pretty=args.pretty)
        if args.markdown_out:
            write_domain_weight_markdown(weight_report, _resolve_cli_path(args.markdown_out, root, must_exist=False))
        print(
            json.dumps(
                {
                    "status": weight_report.get("action_gate_local"),
                    "domain_weight_calibration_status": weight_report.get("domain_weight_calibration_status"),
                    "publication_gate": weight_report.get("publication_gate"),
                    "out": _display_path(out_path, root),
                    "sha256": payload_sha256,
                    "file_sha256": file_sha256,
                },
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        return 0 if weight_report.get("action_gate_local") != "BLOCK" else 2
    if args.command == "nested-backtest":
        root = find_workspace_root(Path.cwd())
        matrix_path = _resolve_cli_path(args.matrix, root, must_exist=True)
        metric_aligned_path = _resolve_cli_path(args.metric_aligned, root, must_exist=True)
        out_path = _resolve_cli_path(args.out, root, must_exist=False)
        matrix_report = json.loads(matrix_path.read_text(encoding="utf-8"))
        metric_aligned_report = json.loads(metric_aligned_path.read_text(encoding="utf-8"))
        nested_report = run_nested_domain_backtest(
            matrix_report.get("objectives", []),
            matrix_report,
            metric_aligned_report,
        )
        payload_sha256, file_sha256 = write_nested_backtest_json(nested_report, out_path, pretty=args.pretty)
        if args.markdown_out:
            write_nested_backtest_markdown(nested_report, _resolve_cli_path(args.markdown_out, root, must_exist=False))
        print(
            json.dumps(
                {
                    "status": nested_report.get("action_gate_local"),
                    "publication_gate": nested_report.get("publication_gate"),
                    "out": _display_path(out_path, root),
                    "sha256": payload_sha256,
                    "file_sha256": file_sha256,
                },
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        return 0 if nested_report.get("action_gate_local") != "BLOCK" else 2
    if args.command == "data-readiness":
        root = find_workspace_root(Path.cwd())
        manifest_path = _resolve_cli_path(args.manifest, root, must_exist=True)
        schema_path = _resolve_cli_path(args.schema, root, must_exist=True)
        out_path = _resolve_cli_path(args.out, root, must_exist=False)
        json.loads(schema_path.read_text(encoding="utf-8"))
        manifest = load_manifest(manifest_path)
        if manifest.get("run_id") == "DUAT_WDI_OFFICIAL_SOURCE_PACK_v0_8":
            readiness_report = build_wdi_source_pack_report(manifest, manifest_path, _sha256_file(manifest_path))
            payload_sha256, file_sha256 = write_wdi_report(readiness_report, out_path, pretty=args.pretty)
        else:
            readiness_report = evaluate_manifest_readiness(manifest)
            payload_sha256, file_sha256 = write_readiness_json(readiness_report, out_path, pretty=args.pretty)
            if args.markdown_out:
                write_readiness_markdown(readiness_report, _resolve_cli_path(args.markdown_out, root, must_exist=False))
        print(
            json.dumps(
                {
                    "status": readiness_report.get("action_gate_local"),
                    "data_gate": readiness_report.get("data_gate"),
                    "publication_gate": readiness_report.get("publication_gate"),
                    "out": _display_path(out_path, root),
                    "sha256": payload_sha256,
                    "file_sha256": file_sha256,
                },
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        return 0
    if args.command == "wdi-source-pack":
        root = find_workspace_root(Path.cwd())
        out_path = _resolve_cli_path(args.out, root, must_exist=False)
        duat_root = root / "research" / "duat-predictive-registry"
        report = run_wdi_source_pack(
            duat_root=duat_root,
            country_code=args.country,
            indicator_codes=args.indicators,
            pretty=args.pretty,
        )
        manifest_errors = validate_wdi_manifest(json.loads((duat_root / "data_sources" / "world_bank_wdi" / "world_bank_wdi_manifest_v0_8.json").read_text(encoding="utf-8")))
        if manifest_errors:
            report["schema_validation"] = "BLOCK"
            report["manifest_errors"] = manifest_errors
        else:
            report["schema_validation"] = "PASS"
            report["manifest_errors"] = []
        payload_sha256, file_sha256 = write_wdi_report(report, out_path, pretty=args.pretty)
        print(
            json.dumps(
                {
                    "status": report.get("action_gate_local"),
                    "data_gate": report.get("data_gate"),
                    "publication_gate": report.get("publication_gate"),
                    "out": _display_path(out_path, root),
                    "sha256": payload_sha256,
                    "file_sha256": file_sha256,
                },
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        return 0
    if args.command == "wdi-governance-review":
        root = find_workspace_root(Path.cwd())
        manifest_path = _resolve_cli_path(args.manifest, root, must_exist=True)
        out_path = _resolve_cli_path(args.out, root, must_exist=False)
        decision = run_wdi_governance_review(
            manifest_path=manifest_path,
            out_path=None,
            pretty=args.pretty,
            verify_external=not args.no_external_verify,
        )
        payload_sha256, file_sha256 = write_governance_json(decision, out_path, pretty=args.pretty)
        print(
            json.dumps(
                {
                    "status": decision.get("action_gate_local", "REVIEW"),
                    "data_gate": decision.get("data_gate"),
                    "backtest_open_gate": decision.get("backtest_open_gate"),
                    "publication_gate": decision.get("publication_gate"),
                    "out": _display_path(out_path, root),
                    "sha256": payload_sha256,
                    "file_sha256": file_sha256,
                },
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        return 0
    return 1


def _resolve_cli_path(path: str, workspace_root: Path, must_exist: bool) -> Path:
    raw = Path(path)
    if raw.is_absolute():
        return raw
    cwd_candidate = (Path.cwd() / raw).resolve()
    if must_exist and cwd_candidate.exists():
        return cwd_candidate
    if not must_exist and (cwd_candidate.parent.exists() or Path.cwd().name == "duat-predictive-registry"):
        return cwd_candidate
    return resolve_workspace_path(raw, workspace_root)


def _display_path(path: Path, workspace_root: Path) -> str:
    try:
        return path.relative_to(workspace_root).as_posix()
    except ValueError:
        return str(path)


def _sha256_file(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
