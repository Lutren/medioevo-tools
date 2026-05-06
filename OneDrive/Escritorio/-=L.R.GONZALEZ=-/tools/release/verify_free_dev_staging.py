from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import venv
from pathlib import Path

from _common import PRODUCTS, ROOT, add_common_args, product_by_name, rel, validate_root_arg
from verify_free_dev_release import BLUEPRINT_REQUIRED, PYTHON_IMPORTS


STAGING_ROOT = ROOT / "publish_staging" / "open-dev"
DEFAULT_OWNER = "Lutren"


def run(command: list[str], cwd: Path) -> dict[str, object]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    return {
        "command": command,
        "cwd": rel(cwd),
        "returncode": result.returncode,
        "stdout_tail": result.stdout.splitlines()[-12:],
        "stderr_tail": result.stderr.splitlines()[-12:],
    }


def venv_python(path: Path) -> Path:
    if sys.platform.startswith("win"):
        return path / "Scripts" / "python.exe"
    return path / "bin" / "python"


def verify_repo(product, temp_root: Path) -> dict[str, object]:
    target = STAGING_ROOT / product.name
    row: dict[str, object] = {
        "name": product.name,
        "target": rel(target),
        "exists": target.exists(),
    }
    if not target.exists():
        row["ok"] = False
        row["reason"] = "missing staging repo"
        return row

    status = run(["git", "status", "--short"], target)
    head = run(["git", "log", "--oneline", "-1"], target)
    remotes = run(["git", "remote", "-v"], target)
    commands = [status, head, remotes]
    expected_remote = f"https://github.com/{DEFAULT_OWNER}/{product.name}.git"
    remote_lines = remotes["stdout_tail"]
    remote_ok = not remote_lines or all(expected_remote in line for line in remote_lines)

    if product.name == "claudio-os-blueprint":
        missing = [name for name in BLUEPRINT_REQUIRED if not (target / name).exists()]
        file_count = sum(1 for path in target.rglob("*") if path.is_file() and ".git" not in path.parts)
        row["blueprint_missing"] = missing
        row["file_count"] = file_count
    elif product.name in PYTHON_IMPORTS:
        venv_dir = temp_root / f"{product.name}-venv"
        smoke_source = temp_root / f"{product.name}-source"
        shutil.copytree(
            target,
            smoke_source,
            ignore=shutil.ignore_patterns(".git", "build", "*.egg-info", "__pycache__", ".pytest_cache"),
        )
        venv.EnvBuilder(with_pip=True, system_site_packages=True).create(venv_dir)
        python_bin = venv_python(venv_dir)
        install = run([str(python_bin), "-m", "pip", "install", "--no-deps", "--no-build-isolation", "."], smoke_source)
        commands.append(install)
        module = PYTHON_IMPORTS[product.name]
        smoke = run([str(python_bin), "-c", f"import {module}; print({module}.__name__)"], smoke_source)
        commands.append(smoke)
        if (smoke_source / "tests").exists():
            commands.append(run([str(python_bin), "-m", "pytest", "tests", "-q"], smoke_source))

    row["commands"] = commands
    row["clean"] = status["returncode"] == 0 and not status["stdout_tail"]
    row["has_remote"] = bool(remote_lines)
    row["remote_ok"] = remote_ok
    row["expected_remote"] = expected_remote
    row["head"] = head["stdout_tail"][0] if head["stdout_tail"] else ""
    row["ok"] = (
        all(item["returncode"] == 0 for item in commands)
        and bool(row["clean"])
        and bool(row["remote_ok"])
        and not row.get("blueprint_missing")
    )
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify local free-dev staging repos.")
    add_common_args(parser)
    parser.add_argument("--product", choices=[p.name for p in PRODUCTS if p.lane == "free-dev"], action="append")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    validate_root_arg(args)

    selected = [product_by_name(name) for name in args.product] if args.product else [p for p in PRODUCTS if p.lane == "free-dev"]
    with tempfile.TemporaryDirectory(prefix="medioevo_free_dev_staging_") as raw_temp:
        temp_root = Path(raw_temp)
        results = [verify_repo(product, temp_root) for product in selected]

    data = {
        "staging_root": rel(STAGING_ROOT),
        "results": results,
        "ok": all(item.get("ok") for item in results),
    }
    if args.write:
        out_dir = ROOT / "qa_artifacts" / "release_validation"
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / "free-dev-staging-smoke.json"
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        data["written"] = rel(target)
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        for item in results:
            status = "ok" if item.get("ok") else "failed"
            print(f"{item['name']}: {status} {item.get('head', '')}")
        if args.write:
            print(f"wrote {data['written']}")
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
