from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from _common import ROOT, rel


APP_DIR = ROOT / "apps" / "commercial" / "argus-desktop"


def tail(text: str, limit: int = 20) -> list[str]:
    return text.splitlines()[-limit:]


def run(command: list[str], cwd: Path) -> dict[str, object]:
    resolved = list(command)
    executable = shutil.which(resolved[0])
    if executable:
        resolved[0] = executable
    try:
        result = subprocess.run(resolved, cwd=cwd, text=True, capture_output=True)
    except FileNotFoundError as exc:
        return {
            "cwd": rel(cwd),
            "command": command,
            "returncode": 127,
            "error": str(exc),
        }
    return {
        "cwd": rel(cwd),
        "command": command,
        "returncode": result.returncode,
        "stdout_tail": tail(result.stdout),
        "stderr_tail": tail(result.stderr),
    }


def verify_install() -> dict[str, object]:
    suffix = ".cmd" if os.name == "nt" else ""
    required_paths = [
        APP_DIR / "node_modules" / ".bin" / f"tsc{suffix}",
        APP_DIR / "node_modules" / ".bin" / f"vite{suffix}",
    ]
    missing = [rel(path) for path in required_paths if not path.exists()]
    if missing:
        return {
            "cwd": rel(APP_DIR),
            "command": ["verify", "argus-dev-binaries"],
            "returncode": 1,
            "missing": missing,
            "stdout_tail": [],
            "stderr_tail": ["required npm binaries missing after install"],
        }
    return {
        "cwd": rel(APP_DIR),
        "command": ["verify", "argus-dev-binaries"],
        "returncode": 0,
        "stdout_tail": ["required npm binaries present"],
        "stderr_tail": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Argus reproducible commercial-app checks.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cache_dir = Path(tempfile.gettempdir()) / "argus-npm-cache-20260429"
    results: list[dict[str, object]] = []

    install = run(["npm", "ci", "--cache", str(cache_dir), "--prefer-online", "--no-audit", "--no-fund"], APP_DIR)
    results.append(install)
    if install.get("returncode") == 0:
        verification = verify_install()
        results.append(verification)
        if verification.get("returncode") != 0:
            fallback = run(
                ["npm", "install", "--include=dev", "--cache", str(cache_dir), "--no-audit", "--no-fund"],
                APP_DIR,
            )
            results.append(fallback)
            if fallback.get("returncode") == 0:
                results.append(verify_install())

    if any(result.get("returncode") != 0 for result in results):
        pass
    else:
        for command in [
            ["npm", "rebuild"],
            ["node", "-e", "require.resolve('workbox-build'); require.resolve('caniuse-lite/dist/unpacker/agents')"],
            ["npm", "run", "typecheck"],
            ["npm", "run", "build"],
            ["npm", "audit", "--omit=dev", "--audit-level=high"],
        ]:
            result = run(command, APP_DIR)
            results.append(result)
            if result.get("returncode") != 0:
                break

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for result in results:
            print(result)
    return 0 if all(result.get("returncode") == 0 for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
