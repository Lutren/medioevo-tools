"""Local cover asset gate for MEDIOEVO editorial candidates.

The gate checks provenance, publication boundaries, dimensions and metadata for
a candidate cover image without approving publication. It is designed to be
safe when no asset exists yet: the result remains REVIEW_ASSET_MISSING.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

try:
    from PIL import Image
except Exception as exc:  # pragma: no cover - host dependency
    Image = None
    PIL_IMPORT_ERROR = exc
else:  # pragma: no cover - import branch
    PIL_IMPORT_ERROR = None


ROOT = Path(__file__).resolve().parents[2]
ALLOWED_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
DEFAULT_MIN_WIDTH = 1000
DEFAULT_MIN_HEIGHT = 1400
SAFE_METADATA_KEYS = {"dpi", "jfif", "jfif_version", "jfif_unit", "jfif_density"}


@dataclass(frozen=True)
class GateFinding:
    severity: str
    code: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return {"severity": self.severity, "code": self.code, "detail": self.detail}


def safe_rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("manifest must be a JSON object")
    return data


def resolve_asset_path(manifest: dict[str, Any], manifest_path: Path, workspace_root: Path) -> Path | None:
    raw = manifest.get("asset_path")
    if raw in (None, ""):
        return None
    path = Path(str(raw))
    if not path.is_absolute():
        path = workspace_root / path
    return path.resolve()


def path_is_under(path: Path, root: Path) -> bool:
    resolved = path.resolve()
    root_resolved = root.resolve()
    return root_resolved in (resolved, *resolved.parents)


def inspect_image(path: Path, workspace_root: Path) -> tuple[dict[str, Any] | None, list[GateFinding]]:
    findings: list[GateFinding] = []
    if Image is None:
        findings.append(
            GateFinding("BLOCK", "IMAGE_LIBRARY_UNAVAILABLE", f"PIL/Pillow is not available: {PIL_IMPORT_ERROR}")
        )
        return None, findings

    try:
        with Image.open(path) as im:
            width, height = im.size
            mode = im.mode
            image_format = im.format
            info_keys = sorted(str(key) for key in im.info.keys())
            exif = im.getexif()
            exif_keys = sorted(str(key) for key in exif.keys())
    except Exception as exc:
        findings.append(GateFinding("BLOCK", "IMAGE_OPEN_FAILED", str(exc)))
        return None, findings

    metadata_keys = sorted({*info_keys, *exif_keys})
    unsafe_metadata_keys = sorted(key for key in metadata_keys if key.lower() not in SAFE_METADATA_KEYS)
    if unsafe_metadata_keys:
        findings.append(
            GateFinding(
                "REVIEW",
                "REVIEW_METADATA_PRESENT",
                "metadata keys present; strip metadata before any public staging",
            )
        )

    if width < DEFAULT_MIN_WIDTH or height < DEFAULT_MIN_HEIGHT:
        findings.append(
            GateFinding(
                "REVIEW",
                "REVIEW_DIMENSIONS_BELOW_DEFAULT",
                f"image is {width}x{height}; default review floor is {DEFAULT_MIN_WIDTH}x{DEFAULT_MIN_HEIGHT}",
            )
        )

    return (
        {
            "path": safe_rel(path, workspace_root),
            "suffix": path.suffix.lower(),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
            "width": width,
            "height": height,
            "mode": mode,
            "format": image_format,
            "metadata_keys_present": metadata_keys,
            "unsafe_metadata_key_count": len(unsafe_metadata_keys),
        },
        findings,
    )


def evaluate_manifest(manifest_path: Path, workspace_root: Path | None = None) -> dict[str, Any]:
    workspace_root = (workspace_root or ROOT).resolve()
    manifest_path = manifest_path.resolve()
    manifest = load_manifest(manifest_path)
    findings: list[GateFinding] = []

    publication_gate = str(manifest.get("publication_gate", "")).upper()
    action_gate = str(manifest.get("action_gate", ""))
    if publication_gate != "BLOCK":
        findings.append(
            GateFinding(
                "BLOCK",
                "PUBLICATION_GATE_NOT_BLOCK",
                "cover assets must keep PublicationGate=BLOCK until a human target-specific approval exists",
            )
        )

    if bool(manifest.get("external_actions_performed", False)):
        findings.append(
            GateFinding("BLOCK", "EXTERNAL_ACTION_REPORTED", "manifest reports external action side effects")
        )

    if str(manifest.get("book_id", "")).strip() == "":
        findings.append(GateFinding("REVIEW", "BOOK_ID_MISSING", "book_id is required"))

    if str(manifest.get("source_provenance", "")).strip() == "":
        findings.append(GateFinding("REVIEW", "SOURCE_PROVENANCE_MISSING", "source_provenance is required"))

    license_status = str(manifest.get("license_status", "")).strip().lower()
    if license_status not in {"owned", "licensed", "owned_or_cleared_for_internal_review"}:
        findings.append(
            GateFinding("REVIEW", "LICENSE_STATUS_REVIEW_REQUIRED", "license_status is not cleared for review")
        )

    asset_path = resolve_asset_path(manifest, manifest_path, workspace_root)
    asset_info: dict[str, Any] | None = None
    if asset_path is None:
        findings.append(GateFinding("REVIEW", "REVIEW_ASSET_MISSING", "no asset_path selected yet"))
    elif not path_is_under(asset_path, workspace_root):
        findings.append(GateFinding("BLOCK", "ASSET_PATH_ESCAPES_WORKSPACE", str(asset_path)))
    elif not asset_path.exists():
        findings.append(GateFinding("REVIEW", "REVIEW_ASSET_MISSING", safe_rel(asset_path, workspace_root)))
    elif asset_path.suffix.lower() not in ALLOWED_SUFFIXES:
        findings.append(
            GateFinding(
                "BLOCK",
                "UNSUPPORTED_ASSET_EXTENSION",
                f"{asset_path.suffix.lower()} is not one of {sorted(ALLOWED_SUFFIXES)}",
            )
        )
    else:
        asset_info, image_findings = inspect_image(asset_path, workspace_root)
        findings.extend(image_findings)

    severities = {finding.severity for finding in findings}
    if "BLOCK" in severities:
        overall_status = "BLOCK_POLICY"
    elif asset_info is None:
        overall_status = "REVIEW_ASSET_MISSING"
    elif "REVIEW" in severities:
        overall_status = "REVIEW_REQUIRED"
    else:
        overall_status = "REVIEW_READY_FOR_HUMAN_VISUAL"

    return {
        "schema_version": "medioevo.cover_asset_gate.result.v1",
        "generated_at": datetime.now().isoformat(),
        "manifest": safe_rel(manifest_path, workspace_root),
        "book_id": manifest.get("book_id"),
        "title": manifest.get("title"),
        "publication_gate": publication_gate or None,
        "action_gate": action_gate or None,
        "overall_status": overall_status,
        "asset": asset_info,
        "manual_text_check_required": True,
        "manual_visual_boundary_check_required": True,
        "metadata_strip_required": any(finding.code == "REVIEW_METADATA_PRESENT" for finding in findings),
        "external_actions_performed": bool(manifest.get("external_actions_performed", False)),
        "findings": [finding.as_dict() for finding in findings],
        "not_publication_approval": True,
    }


def write_report(result: dict[str, Any], out_path: Path) -> None:
    asset = result.get("asset") or {}
    lines = [
        f"# Cover Asset Gate - {date.today().isoformat()}",
        "",
        f"Status: `{result['overall_status']}`",
        "",
        f"- Book: `{result.get('book_id')}`",
        f"- Title: `{result.get('title')}`",
        f"- PublicationGate: `{result.get('publication_gate')}`",
        f"- ActionGate: `{result.get('action_gate')}`",
        f"- Manifest: `{result.get('manifest')}`",
        f"- External actions performed: `{str(result.get('external_actions_performed')).lower()}`",
        f"- Not publication approval: `{str(result.get('not_publication_approval')).lower()}`",
        "",
    ]
    if asset:
        lines.extend(
            [
                "## Asset",
                "",
                f"- Path: `{asset.get('path')}`",
                f"- Dimensions: `{asset.get('width')}x{asset.get('height')}`",
                f"- Format: `{asset.get('format')}`",
                f"- SHA256: `{asset.get('sha256')}`",
                f"- Metadata keys present: `{len(asset.get('metadata_keys_present', []))}`",
                "",
            ]
        )
    else:
        lines.extend(["## Asset", "", "- No asset selected or readable yet.", ""])

    lines.extend(["## Findings", ""])
    findings = result.get("findings", [])
    if findings:
        for finding in findings:
            lines.append(f"- `{finding['severity']}` `{finding['code']}`: {finding['detail']}")
    else:
        lines.append("- No policy block found. Human visual/text/licensing review is still required.")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This report does not approve KDP, Gumroad, web, social, push, deploy or public ZIP actions.",
            "- Manual review must confirm no readable manuscript text, no private diagrams, no RPG/TCG assets, no local paths and no proprietary claim leakage.",
            "- Keep `PublicationGate=BLOCK` until a target-specific human approval exists.",
            "",
        ]
    )
    out_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="cover asset gate manifest JSON")
    parser.add_argument("--out-dir", default=None, help="directory for JSON/Markdown reports")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest)
    result = evaluate_manifest(manifest_path, ROOT)
    out_dir = Path(args.out_dir) if args.out_dir else manifest_path.resolve().parent
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = out_dir / "cover_asset_gate_summary.json"
    report_path = out_dir / f"COVER_ASSET_GATE_REPORT_{date.today().isoformat()}.md"
    summary_path.write_text(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=True), encoding="utf-8")
    write_report(result, report_path)
    print(
        json.dumps(
            {
                "overall_status": result["overall_status"],
                "summary": safe_rel(summary_path, ROOT),
                "report": safe_rel(report_path, ROOT),
                "finding_count": len(result["findings"]),
            },
            indent=2,
        )
    )
    if result["overall_status"] == "BLOCK_POLICY":
        return 3
    if result["overall_status"] in {"REVIEW_ASSET_MISSING", "REVIEW_REQUIRED"}:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
