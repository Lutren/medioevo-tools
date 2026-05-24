from __future__ import annotations

import argparse

from _common import ROOT, add_common_args, print_json, run_command, validate_root_arg


COMMANDS = [
    {
        "name": "obsai-core-pytest",
        "cwd": "packages/open-dev/obsai-core",
        "command": ["python", "-m", "pytest", "tests", "-q"],
        "private": False,
    },
    {
        "name": "residueos-pytest",
        "cwd": "packages/open-dev/residueos",
        "command": ["python", "-m", "pytest", "tests", "-q"],
        "private": False,
    },
    {
        "name": "gemma-cleanup-pytest",
        "cwd": "packages/open-dev/gemma-observacionismo-cleanup",
        "command": ["python", "-m", "pytest", "tests", "-q"],
        "private": False,
    },
    {
        "name": "obs-safe-integration-kit-pytest",
        "cwd": "packages/open-dev/obs-safe-integration-kit",
        "command": ["python", "-m", "pytest", "tests", "-q"],
        "private": False,
    },
    {
        "name": "duat-genesis-pytest",
        "cwd": "packages/open-dev/duat-genesis",
        "command": ["python", "-m", "pytest", "tests", "-q"],
        "private": False,
    },
    {
        "name": "geodia-social-observatory-pytest",
        "cwd": "research/geodia-social-observatory",
        "command": ["python", "-m", "pytest", "tests", "-q"],
        "private": False,
    },
    {
        "name": "observacionismo-gate-import",
        "cwd": "packages/open-dev/observacionismo-gate",
        "command": ["python", "-c", "import observacionismo_gate; print(observacionismo_gate.__name__)"],
        "private": False,
    },
    {
        "name": "mini-office-pytest",
        "cwd": "apps/commercial/mini-office",
        "command": ["python", "-m", "pytest", "tests", "-q"],
        "private": False,
    },
    {
        "name": "claudio-pytest",
        "cwd": "-=MEDIOEVO=-/-=LIBROS/claudio",
        "command": ["python", "-m", "pytest", "tests/", "-x", "--quiet"],
        "private": False,
    },
    {
        "name": "argus-npm-ci-dry-run",
        "cwd": "apps/commercial/argus-desktop",
        "command": ["npm", "ci", "--dry-run", "--ignore-scripts", "--no-audit", "--no-fund"],
        "private": False,
    },
    {
        "name": "asistente-negocio-check",
        "cwd": "apps/commercial/asistente-negocio",
        "command": ["npm", "run", "check"],
        "private": False,
    },
    {
        "name": "flujocrm-check",
        "cwd": "apps/commercial/flujocrm",
        "command": ["npm", "run", "check"],
        "private": False,
    },
    {
        "name": "hormiguero-flask-smoke",
        "cwd": ".",
        "command": ["python", "tools/release/hormiguero_smoke.py"],
        "private": False,
    },
    {
        "name": "private-metaevo-lint",
        "cwd": "-=MEDIOEVO=-/-=LIBROS/metaevo-tcg",
        "command": ["npm", "run", "lint"],
        "private": True,
    },
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run or execute known test commands.")
    add_common_args(parser)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--include-private", action="store_true", help="include private game checks")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    validate_root_arg(args)

    results = []
    for item in COMMANDS:
        if item.get("private") and not args.include_private:
            results.append({"name": item["name"], "skipped": "private_check_requires_include_private"})
            continue
        cwd = ROOT / item["cwd"]
        if not cwd.exists():
            results.append({"name": item["name"], "missing": item["cwd"]})
            continue
        result = run_command(item["command"], cwd, execute=args.execute)
        result["name"] = item["name"]
        results.append(result)
    if args.json:
        print_json(results)
    else:
        for row in results:
            print(row)
    return 0 if not args.execute or all(row.get("returncode", 0) == 0 for row in results if row.get("executed")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
