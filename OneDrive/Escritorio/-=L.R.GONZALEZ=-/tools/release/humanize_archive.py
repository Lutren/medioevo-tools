from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.release.lobby_absorption import (
    LobbyRecord,
    lane_folder_name,
    render_report,
    render_retirements,
    sha256_file,
    summarize,
    write_human_archive_index,
)


def load_manifest(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def move_record(record: LobbyRecord, archive_root: Path, write: bool) -> tuple[LobbyRecord, bool]:
    if not record.archived_path:
        return record, False

    current_path = Path(record.archived_path)
    destination = archive_root / lane_folder_name(record.lane) / current_path.name

    if current_path.resolve() == destination.resolve():
        if sha256_file(destination) != record.sha256:
            raise RuntimeError(f"archive_hash_mismatch: {destination}")
        return record, False

    if destination.exists():
        if sha256_file(destination) != record.sha256:
            raise RuntimeError(f"destination_collision: {destination}")
        record.archived_path = str(destination)
        return record, False

    if not current_path.exists():
        raise FileNotFoundError(f"archived_source_missing: {current_path}")

    if sha256_file(current_path) != record.sha256:
        raise RuntimeError(f"archive_hash_mismatch: {current_path}")

    if write:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(current_path), str(destination))
        if sha256_file(destination) != record.sha256:
            raise RuntimeError(f"archive_hash_mismatch_after_move: {destination}")
        record.archived_path = str(destination)
    return record, True


def humanize_manifest(manifest_path: Path, archive_root: Path, write: bool) -> dict[str, object]:
    payload = load_manifest(manifest_path)
    records = [LobbyRecord(**record) for record in payload["records"]]  # type: ignore[arg-type]
    moved = 0
    updated_records: list[LobbyRecord] = []
    for record in records:
        updated, was_moved = move_record(record, archive_root, write)
        moved += int(was_moved)
        updated_records.append(updated)

    updated_payload = {
        "schema": payload.get("schema", "medioevo.lobby_alejandria.absorption.v1"),
        "generated_at_utc": payload.get("generated_at_utc"),
        "records": [record.__dict__ for record in updated_records],
        "summary": summarize(updated_records),
    }

    if write:
        manifest_path.write_text(json.dumps(updated_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        report_path = manifest_path.with_name(manifest_path.name.replace("_MANIFEST.json", "_REPORT.md"))
        retirements_path = manifest_path.with_name(manifest_path.name.replace("_MANIFEST.json", "_RETIREMENTS.md"))
        report_path.write_text(render_report(updated_payload), encoding="utf-8")
        retirements_path.write_text(render_retirements(updated_records), encoding="utf-8")
        write_human_archive_index(updated_records, archive_root)

    return {
        "manifest": str(manifest_path),
        "archive_root": str(archive_root),
        "records": len(updated_records),
        "moved": moved,
        "write": write,
        "folders": sorted({lane_folder_name(record.lane) for record in updated_records if record.archived_path}),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reorganize Archivo Frio sources into human-readable lane folders.")
    parser.add_argument("--manifest", required=True, help="Absorption manifest to update.")
    parser.add_argument("--archive-root", required=True, help="Archivo Frio root for this source/date.")
    parser.add_argument("--write", action="store_true", help="Apply moves and update reports.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = parse_args(argv)
    result = humanize_manifest(Path(args.manifest).resolve(), Path(args.archive_root).resolve(), args.write)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"manifest: {result['manifest']}")
        print(f"archive_root: {result['archive_root']}")
        print(f"records: {result['records']}")
        print(f"moved: {result['moved']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
