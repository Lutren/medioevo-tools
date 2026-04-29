from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path

from _common import ROOT, ensure_under_root, print_json, rel


ARGUS_ARTIFACTS = [
    ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "apps" / "argus_desktop" / "node_modules",
    ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "apps" / "argus_desktop" / "dist",
    ROOT / "apps" / "commercial" / "argus-desktop" / "node_modules",
    ROOT / "apps" / "commercial" / "argus-desktop" / "dist",
]


def archive_target(source: Path, archive_root: Path) -> Path:
    name = source.name
    target = archive_root / name
    if not target.exists():
        return target
    suffix = datetime.utcnow().strftime("%H%M%S")
    return archive_root / f"{name}_{suffix}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive generated artifacts with an explicit --execute gate.")
    parser.add_argument("--execute", action="store_true", help="move artifacts into _archive")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    archive_root = ensure_under_root(
        ROOT / "_archive" / "legacy" / "2026-04-29" / "argus_generated_artifacts_second_pass"
    )
    rows: list[dict[str, object]] = []
    for source in ARGUS_ARTIFACTS:
        source = ensure_under_root(source)
        if not source.exists():
            rows.append({"source": rel(source), "exists": False, "action": "skip_missing"})
            continue
        target = archive_target(source, archive_root)
        target = ensure_under_root(target)
        row = {
            "source": rel(source),
            "destination": rel(target),
            "exists": True,
            "executed": args.execute,
        }
        if args.execute:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(target))
            row["action"] = "moved_to_archive"
        else:
            row["action"] = "dry_run"
        rows.append(row)

    if args.json:
        print_json(rows)
    else:
        for row in rows:
            print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
