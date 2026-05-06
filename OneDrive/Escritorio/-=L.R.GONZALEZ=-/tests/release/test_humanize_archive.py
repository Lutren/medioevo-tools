from __future__ import annotations

import json
from pathlib import Path

from tools.release import humanize_archive, lobby_absorption


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_humanize_archive_moves_sources_by_lane_and_updates_manifest(tmp_path):
    archive_root = tmp_path / "archive"
    flat_source = archive_root / "ABCDEF0123456789_matrix.txt"
    write(flat_source, "MISION: Matrix\nWitnessLog\n")
    sha256 = lobby_absorption.sha256_file(flat_source)
    manifest = tmp_path / "docs" / "fixture_MANIFEST.json"
    payload = {
        "schema": "medioevo.lobby_alejandria.absorption.v1",
        "generated_at_utc": "2026-05-06T00:00:00+00:00",
        "records": [
            {
                "original_path": "C:/Lobby/matrix.txt",
                "archived_path": str(flat_source),
                "filename": "matrix.txt",
                "sha256": sha256,
                "size_bytes": flat_source.stat().st_size,
                "line_count": 2,
                "character_count": len(flat_source.read_text(encoding="utf-8")),
                "lane": "Matrix/Biblioteca",
                "psi_state": "INFERENCIA",
                "action_gate": "REVIEW",
                "status": "ABSORBIDO_ARCHIVO_FRIO",
                "decision": "ABSORB_TO_ATLAS_AND_ARCHIVE_SOURCE",
                "target_artifacts": ["docs/matrix"],
                "evidence_markers": ["matrix"],
                "extracted_patterns": ["MISION: Matrix"],
                "falsifiers": ["sha256_mismatch"],
                "risk_flags": [],
            }
        ],
        "summary": {},
    }
    write(manifest, json.dumps(payload, indent=2))

    result = humanize_archive.humanize_manifest(manifest, archive_root, write=True)

    assert result["moved"] == 1
    moved_path = archive_root / "04_matrix_biblioteca" / flat_source.name
    assert moved_path.exists()
    assert not flat_source.exists()
    assert lobby_absorption.sha256_file(moved_path) == sha256
    updated = json.loads(manifest.read_text(encoding="utf-8"))
    assert updated["records"][0]["archived_path"] == str(moved_path)
    assert (archive_root / "00_LEER_PRIMERO.md").exists()


def test_humanize_archive_is_idempotent(tmp_path):
    archive_root = tmp_path / "archive"
    lane_path = archive_root / "04_matrix_biblioteca" / "ABCDEF0123456789_matrix.txt"
    write(lane_path, "MISION: Matrix\n")
    sha256 = lobby_absorption.sha256_file(lane_path)
    manifest = tmp_path / "fixture_MANIFEST.json"
    write(
        manifest,
        json.dumps(
            {
                "schema": "medioevo.lobby_alejandria.absorption.v1",
                "generated_at_utc": "2026-05-06T00:00:00+00:00",
                "records": [
                    {
                        "original_path": "C:/Lobby/matrix.txt",
                        "archived_path": str(lane_path),
                        "filename": "matrix.txt",
                        "sha256": sha256,
                        "size_bytes": lane_path.stat().st_size,
                        "line_count": 1,
                        "character_count": len(lane_path.read_text(encoding="utf-8")),
                        "lane": "Matrix/Biblioteca",
                        "psi_state": "INFERENCIA",
                        "action_gate": "REVIEW",
                        "status": "ABSORBIDO_ARCHIVO_FRIO",
                        "decision": "ABSORB_TO_ATLAS_AND_ARCHIVE_SOURCE",
                        "target_artifacts": ["docs/matrix"],
                        "evidence_markers": ["matrix"],
                        "extracted_patterns": ["MISION: Matrix"],
                        "falsifiers": ["sha256_mismatch"],
                        "risk_flags": [],
                    }
                ],
                "summary": {},
            },
            indent=2,
        ),
    )

    result = humanize_archive.humanize_manifest(manifest, archive_root, write=True)

    assert result["moved"] == 0
    assert lane_path.exists()
