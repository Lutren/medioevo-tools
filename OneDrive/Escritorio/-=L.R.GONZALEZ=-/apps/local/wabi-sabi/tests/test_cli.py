import json
import os
import subprocess
import sys
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args, workspace: Path, runtime: Path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(APP_ROOT)
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "wabi_sabi.cli.main",
            *args,
            "--workspace",
            str(workspace),
            "--runtime",
            str(runtime),
        ],
        cwd=str(APP_ROOT),
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
    )


def test_cli_e2e_smoke_logs_and_routes(tmp_path):
    proc = run_cli("e2e-smoke", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["intent"] == "code_generation"
    assert payload["agent"] == "programmer"
    assert payload["artifacts"]
    assert Path(payload["log"]).exists()


def test_cli_agents_command(tmp_path):
    proc = run_cli("agents", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert "programmer" in payload["agents"]
    assert "debugger" in payload["agents"]


def test_cli_apply_programs_python_file(tmp_path):
    proc = run_cli(
        "crea una funcion que lea un archivo y resuma sus lineas",
        "--apply",
        "--target",
        "helpers.py",
        "--json",
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
    )

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["action"] == "scoped_code_patch_applied"
    assert (tmp_path / "helpers.py").exists()
    assert "summarize_file_lines" in (tmp_path / "helpers.py").read_text(encoding="utf-8")


def test_cli_codex_status_and_dry_run(tmp_path):
    status_proc = run_cli("codex-status", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert status_proc.returncode == 0, status_proc.stderr
    status = json.loads(status_proc.stdout)
    assert "auto_provider" in status
    assert "safe_default" in status

    dry_proc = run_cli(
        "codex",
        "responde una prueba corta",
        "--dry-run",
        "--json",
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
    )

    assert dry_proc.returncode == 0, dry_proc.stderr
    payload = json.loads(dry_proc.stdout)
    assert payload["action"] == "codex_bridge_dry_run"
    assert payload["artifacts"]
