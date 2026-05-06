from __future__ import annotations

from pathlib import Path

from tools.release import claudio_root_human_audit


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_claudio_root_human_audit_classifies_root_noise(tmp_path):
    write(tmp_path / "core" / "x.py", "pass")
    write(tmp_path / "INICIAR.bat", "echo hi")
    write(tmp_path / "note.md", "# note")
    write(tmp_path / ".env", "SECRET=redacted")
    write(tmp_path / "local.db", "db")
    write(tmp_path / "tool.py", "print('x')")

    payload = claudio_root_human_audit.build_audit(tmp_path)
    by_name = {record["name"]: record for record in payload["records"]}

    assert by_name["core"]["decision"] == "KEEP"
    assert by_name["INICIAR.bat"]["category"] == "launcher_script"
    assert by_name["note.md"]["destination_hint"] == "docs/root_notes_review"
    assert by_name[".env"]["decision"] == "BLOCK_MOVE_TO_PRIVATE_CONFIG"
    assert by_name["local.db"]["category"] == "local_state_db"
    assert by_name["tool.py"]["destination_hint"] == "tools/root_scripts_review"


def test_claudio_root_human_audit_writes_outputs(tmp_path):
    target = tmp_path / "claudio"
    target.mkdir()
    write(target / "core" / "x.py", "pass")
    output = tmp_path / "out"

    payload = claudio_root_human_audit.build_audit(target)
    paths = claudio_root_human_audit.write_outputs(payload, output)

    assert Path(paths["manifest"]).exists()
    assert Path(paths["audit"]).exists()
    assert Path(paths["plan"]).exists()
