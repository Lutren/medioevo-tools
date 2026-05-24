from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "release"))

import validate_cover_asset_gate as gate  # noqa: E402


def write_manifest(path: Path, **overrides: object) -> Path:
    data = {
        "schema_version": "medioevo.cover_asset_gate.v1",
        "book_id": "03_FRAGMENTOS",
        "title": "MEDIOEVO: Fragmentos",
        "publication_gate": "BLOCK",
        "action_gate": "REVIEW_ASSET_PRODUCTION",
        "asset_path": None,
        "source_type": "not_selected",
        "source_provenance": "pending_human_review",
        "license_status": "pending_review",
        "external_actions_performed": False,
    }
    data.update(overrides)
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_missing_asset_stays_in_review_without_publication_approval(tmp_path: Path) -> None:
    manifest = write_manifest(tmp_path / "manifest.json")

    result = gate.evaluate_manifest(manifest, workspace_root=tmp_path)

    assert result["overall_status"] == "REVIEW_ASSET_MISSING"
    assert result["publication_gate"] == "BLOCK"
    assert result["not_publication_approval"] is True
    assert {finding["code"] for finding in result["findings"]} >= {
        "REVIEW_ASSET_MISSING",
        "LICENSE_STATUS_REVIEW_REQUIRED",
    }


def test_clean_local_asset_becomes_human_visual_review_ready(tmp_path: Path) -> None:
    asset = tmp_path / "fragmentos-cover.png"
    Image.new("RGB", (1600, 2400), "white").save(asset)
    manifest = write_manifest(
        tmp_path / "manifest.json",
        asset_path=asset.name,
        source_type="owned_test_fixture",
        source_provenance="synthetic local test fixture",
        license_status="owned_or_cleared_for_internal_review",
    )

    result = gate.evaluate_manifest(manifest, workspace_root=tmp_path)

    assert result["overall_status"] == "REVIEW_READY_FOR_HUMAN_VISUAL"
    assert result["asset"]["width"] == 1600
    assert result["asset"]["height"] == 2400
    assert result["manual_text_check_required"] is True
    assert result["manual_visual_boundary_check_required"] is True
    assert result["not_publication_approval"] is True


def test_open_publication_gate_blocks_asset(tmp_path: Path) -> None:
    asset = tmp_path / "fragmentos-cover.png"
    Image.new("RGB", (1600, 2400), "white").save(asset)
    manifest = write_manifest(
        tmp_path / "manifest.json",
        asset_path=asset.name,
        source_provenance="synthetic local test fixture",
        license_status="owned_or_cleared_for_internal_review",
        publication_gate="APPROVE",
    )

    result = gate.evaluate_manifest(manifest, workspace_root=tmp_path)

    assert result["overall_status"] == "BLOCK_POLICY"
    assert "PUBLICATION_GATE_NOT_BLOCK" in {finding["code"] for finding in result["findings"]}
