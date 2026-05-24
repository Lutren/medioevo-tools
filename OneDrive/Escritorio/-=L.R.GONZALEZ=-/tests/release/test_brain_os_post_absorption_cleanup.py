from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATRIX_JSON = ROOT / "docs" / "intake" / "BRAIN_OS_POST_ABSORPTION_CLEANUP_POSTERIOR_2026-05-18.json"
MATRIX_MD = ROOT / "docs" / "intake" / "BRAIN_OS_POST_ABSORPTION_CLEANUP_POSTERIOR_2026-05-18.md"
REGISTER = ROOT / "SOURCE_INTAKE_REGISTER.md"

EXPECTED_PORTFOLIO_SETS = {
    "post_medi_portfolio",
    "brain_os_identity_portfolio",
    "osit_agent_knowledge_portfolio",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def iter_files(path: Path) -> list[Path]:
    denied_names = {".git", "node_modules", ".venv", "__pycache__", ".pytest_cache"}
    return [
        child
        for child in sorted(path.rglob("*"))
        if child.is_file() and not any(part in denied_names for part in child.parts)
    ]


def sha256_dir(path: Path) -> str:
    digest = hashlib.sha256()
    for child in iter_files(path):
        rel_path = child.relative_to(path).as_posix()
        digest.update(rel_path.encode("utf-8", "surrogatepass"))
        digest.update(b"\0")
        digest.update(str(child.stat().st_size).encode("ascii"))
        digest.update(b"\0")
        digest.update(sha256_file(child).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest().upper()


def load_matrix() -> dict:
    return json.loads(MATRIX_JSON.read_text(encoding="utf-8"))


def test_matrix_records_exact_paths_and_current_hashes() -> None:
    matrix = load_matrix()

    assert matrix["schema"] == "medioevo.brain_os_post_absorption_cleanup.v1"
    assert matrix["source_count"] == len(matrix["sources"])
    assert matrix["source_count"] >= 19

    for source in matrix["sources"]:
        path = Path(source["path"])
        assert path.exists(), source["path"]
        if source["hash_kind"] == "file_sha256":
            assert source["sha256"] == sha256_file(path)
        elif source["hash_kind"] == "directory_tree_sha256":
            assert source["sha256"] == sha256_dir(path)
        else:
            raise AssertionError(f"unexpected hash kind: {source['hash_kind']}")


def test_three_portfolio_sets_are_explicit_and_gated() -> None:
    matrix = load_matrix()

    assert set(matrix["portfolio_sets"]) == EXPECTED_PORTFOLIO_SETS
    assert matrix["portfolio_set_count"] == 3

    for portfolio_id, paths in matrix["portfolio_sets"].items():
        assert paths, portfolio_id
        for path in paths:
            assert Path(path).exists()

    portfolio_sources = [source for source in matrix["sources"] if source["portfolio_set"]]
    assert portfolio_sources
    for source in portfolio_sources:
        assert source["publication_gate"] == "BLOCK"
        assert source["runtime_import"] == "BLOCK"
        assert source["raw_adoption"] == "BLOCK"


def test_gates_block_publication_runtime_import_and_raw_adoption() -> None:
    matrix = load_matrix()
    gates = matrix["gate_summary"]

    assert gates["PublicationGate"] == "BLOCK"
    assert gates["RuntimeImportGate"] == "BLOCK"
    assert gates["RawAdoption"] == "BLOCK"
    assert gates["MigrationMoveDelete"] == "BLOCK_WITHOUT_MIGRATION_LOG_ROLLBACK_ACTIONGATE"

    combined = MATRIX_MD.read_text(encoding="utf-8") + "\n" + json.dumps(matrix, ensure_ascii=False)
    assert "PublicationGate=APPROVE" not in combined
    assert "RuntimeImport=APPROVE" not in combined
    assert "RawAdoption=APPROVE" not in combined


def test_every_source_has_ficha_and_register_entry() -> None:
    matrix = load_matrix()
    register_text = REGISTER.read_text(encoding="utf-8")

    for source in matrix["sources"]:
        ficha = ROOT / source["ficha"]
        assert ficha.exists(), source["ficha"]
        ficha_text = ficha.read_text(encoding="utf-8")
        assert source["path"] in ficha_text
        assert source["sha256"] in ficha_text
        assert "RawAdoption: `BLOCK`" in ficha_text
        assert source["path"] in register_text
        assert source["sha256"] in register_text


def test_delta_matrix_has_required_curator_columns() -> None:
    matrix = load_matrix()
    sources = {source["path"]: source for source in matrix["sources"]}
    required = {
        "source_path",
        "source_sha256",
        "unique_contribution",
        "conflict",
        "strong_claim_boundary",
        "falsifier",
        "destination",
        "state",
        "action_gate",
    }

    for delta in matrix["delta_matrix"]:
        missing = [field for field in required if not delta.get(field)]
        assert missing == [], f"{delta['id']} missing {missing}"
        assert delta["source_path"] in sources
        assert delta["source_sha256"] == sources[delta["source_path"]]["sha256"]
        assert delta["action_gate"] in {"APPROVE_LOCAL_DOCS_ONLY", "REVIEW", "BLOCK"}


def test_no_raw_source_hash_was_copied_to_runtime_apps_or_packages() -> None:
    matrix = load_matrix()

    assert matrix["raw_copy_check"]
    for check in matrix["raw_copy_check"]:
        assert check["status"] == "PASS_NO_RAW_SOURCE_HASH_MATCH"
        assert check["matches"] == []


def test_duplicate_candidates_are_review_only() -> None:
    matrix = load_matrix()

    for candidate in matrix["duplicate_candidates"]:
        assert candidate["gate"] == "REVIEW_BEFORE_MIGRATION"
        assert candidate["action"] == "document only; no move/delete executed"
        assert len(candidate["paths"]) >= 2
