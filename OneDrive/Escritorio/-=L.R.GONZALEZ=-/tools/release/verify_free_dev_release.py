from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import venv
from pathlib import Path
from zipfile import ZipFile

from _common import PRODUCTS, ROOT, add_common_args, collect_product_files, product_by_name, rel, sha256_file, validate_root_arg


PYTHON_IMPORTS = {
    "obsai-core": "obsai_core",
    "residueos": "residueos",
    "observacionismo-gate": "observacionismo_gate",
    "gemma-observacionismo-cleanup": "gemma_observacionismo_cleanup",
    "duat-genesis": "duat_genesis",
}

BLUEPRINT_REQUIRED = (
    "README.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "docs/ARCHITECTURE.md",
    "docs/ROADMAP.md",
)


def run(command: list[str], cwd: Path) -> dict[str, object]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    return {
        "command": command,
        "cwd": str(cwd),
        "returncode": result.returncode,
        "stdout_tail": result.stdout.splitlines()[-10:],
        "stderr_tail": result.stderr.splitlines()[-10:],
    }


def venv_python(path: Path) -> Path:
    if sys.platform.startswith("win"):
        return path / "Scripts" / "python.exe"
    return path / "bin" / "python"


def verify_members(product, zip_path: Path) -> dict[str, object]:
    expected = sorted(rel(path) for path in collect_product_files(product)[0])
    with ZipFile(zip_path) as archive:
        actual = sorted(name for name in archive.namelist() if not name.endswith("/"))
    return {
        "expected_count": len(expected),
        "actual_count": len(actual),
        "missing": [name for name in expected if name not in actual],
        "unexpected": [name for name in actual if name not in expected],
    }


def verify_product(product, temp_root: Path, python_bin: Path | None) -> dict[str, object]:
    zip_path = ROOT / "releases" / "free-dev" / f"{product.name}.zip"
    row: dict[str, object] = {
        "name": product.name,
        "zip": rel(zip_path),
        "exists": zip_path.exists(),
    }
    if not zip_path.exists():
        row["ok"] = False
        row["reason"] = "missing zip"
        return row

    row["bytes"] = zip_path.stat().st_size
    row["sha256"] = sha256_file(zip_path)
    row["members"] = verify_members(product, zip_path)
    extract_dir = temp_root / product.name
    extract_dir.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path) as archive:
        archive.extractall(extract_dir)

    product_dir = extract_dir / product.source
    row["extracted_source_exists"] = product_dir.exists()
    commands = []

    if product.name == "claudio-os-blueprint":
        missing = [name for name in BLUEPRINT_REQUIRED if not (product_dir / name).exists()]
        row["blueprint_missing"] = missing
    elif product.name in PYTHON_IMPORTS:
        if python_bin is None:
            row["ok"] = False
            row["reason"] = "missing venv python"
            return row
        install = run([str(python_bin), "-m", "pip", "install", "--no-deps", "--no-build-isolation", str(product_dir)], temp_root)
        commands.append(install)
        module = PYTHON_IMPORTS[product.name]
        smoke = run([str(python_bin), "-c", f"import {module}; print({module}.__name__)"], temp_root)
        commands.append(smoke)

    row["commands"] = commands
    member_ok = not row["members"]["missing"] and not row["members"]["unexpected"]
    command_ok = all(item.get("returncode") == 0 for item in commands)
    blueprint_ok = not row.get("blueprint_missing")
    row["ok"] = bool(member_ok and command_ok and blueprint_ok and row["extracted_source_exists"])
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify free-dev ZIP artifacts from clean temporary extraction.")
    add_common_args(parser)
    parser.add_argument("--product", choices=[p.name for p in PRODUCTS if p.lane == "free-dev"], action="append")
    parser.add_argument("--write", action="store_true", help="write qa_artifacts/release_validation/free-dev-smoke.json")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    validate_root_arg(args)

    selected = [product_by_name(name) for name in args.product] if args.product else [p for p in PRODUCTS if p.lane == "free-dev"]
    with tempfile.TemporaryDirectory(prefix="medioevo_free_dev_smoke_") as raw_temp:
        temp_root = Path(raw_temp)
        venv_dir = temp_root / ".venv"
        venv.EnvBuilder(with_pip=True, system_site_packages=True).create(venv_dir)
        python_bin = venv_python(venv_dir)
        if not python_bin.exists():
            python_bin = None
        results = [verify_product(product, temp_root, python_bin) for product in selected]

    data = {
        "artifact_lane": "free-dev",
        "zip_root": rel(ROOT / "releases" / "free-dev"),
        "results": results,
        "ok": all(item.get("ok") for item in results),
    }
    if args.write:
        out_dir = ROOT / "qa_artifacts" / "release_validation"
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / "free-dev-smoke.json"
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        data["written"] = rel(target)
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        for item in results:
            status = "ok" if item.get("ok") else "failed"
            print(f"{item['name']}: {status} {item.get('sha256', '')}")
        if args.write:
            print(f"wrote {data['written']}")
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
