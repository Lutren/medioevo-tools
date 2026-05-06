from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from _common import PRODUCTS, ROOT, add_common_args, collect_product_files, product_by_name, rel, validate_root_arg


STAGING_ROOT = ROOT / "publish_staging" / "open-dev"
DEFAULT_COMMIT = "Initial public release staging"
GIT_NAME = "L.R. Gonzalez"
GIT_EMAIL = "lutren@users.noreply.github.com"


def run(command: list[str], cwd: Path) -> dict[str, object]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    return {
        "command": command,
        "cwd": rel(cwd),
        "returncode": result.returncode,
        "stdout_tail": result.stdout.splitlines()[-12:],
        "stderr_tail": result.stderr.splitlines()[-12:],
    }


def copy_allowlisted_files(product, target: Path) -> list[str]:
    files, blocked, _excluded = collect_product_files(product)
    if blocked:
        reasons = ", ".join(f"{path}:{reason}" for path, reason in blocked[:10])
        raise RuntimeError(f"{product.name} has blocked files: {reasons}")

    copied: list[str] = []
    source_root = product.source_path.resolve()
    target.mkdir(parents=True, exist_ok=True)
    for path in files:
        relative = path.resolve().relative_to(source_root)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
        copied.append(relative.as_posix())
    return copied


def existing_repo_status(target: Path) -> dict[str, object]:
    if not (target / ".git").exists():
        return {"exists": target.exists(), "is_repo": False}
    status = run(["git", "status", "--short"], target)
    remotes = run(["git", "remote", "-v"], target)
    head = run(["git", "log", "--oneline", "-1"], target)
    return {
        "exists": True,
        "is_repo": True,
        "status": status,
        "remotes": remotes,
        "head": head,
        "clean": status["returncode"] == 0 and not status["stdout_tail"],
    }


def stage_product(product, *, skip_existing: bool) -> dict[str, object]:
    target = STAGING_ROOT / product.name
    row: dict[str, object] = {
        "name": product.name,
        "source": product.source,
        "target": rel(target),
    }
    existing = existing_repo_status(target)
    if existing.get("exists") and skip_existing:
        row["skipped"] = "target_exists"
        row["existing"] = existing
        return row
    if existing.get("exists"):
        row["ok"] = False
        row["reason"] = "target exists; rerun with --skip-existing or choose manual review"
        row["existing"] = existing
        return row

    copied = copy_allowlisted_files(product, target)
    commands = [
        run(["git", "init", "-b", "main"], target),
        run(["git", "config", "user.name", GIT_NAME], target),
        run(["git", "config", "user.email", GIT_EMAIL], target),
    ]
    if copied:
        commands.append(run(["git", "add", "--", *copied], target))
    commands.append(run(["git", "diff", "--cached", "--check"], target))
    if all(item["returncode"] == 0 for item in commands):
        commands.append(run(["git", "commit", "-m", DEFAULT_COMMIT], target))
    status = run(["git", "status", "--short"], target)
    head = run(["git", "log", "--oneline", "-1"], target)
    remotes = run(["git", "remote", "-v"], target)
    row.update(
        {
            "copied_files": copied,
            "file_count": len(copied),
            "commands": commands,
            "status": status,
            "head": head,
            "remotes": remotes,
            "ok": all(item["returncode"] == 0 for item in commands) and status["returncode"] == 0 and not status["stdout_tail"],
        }
    )
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description="Create clean local Git staging repos for free-dev products.")
    add_common_args(parser)
    parser.add_argument("--product", choices=[p.name for p in PRODUCTS if p.lane == "free-dev"], action="append")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    validate_root_arg(args)

    selected = [product_by_name(name) for name in args.product] if args.product else [p for p in PRODUCTS if p.lane == "free-dev"]
    results = [stage_product(product, skip_existing=args.skip_existing) for product in selected]
    data = {
        "staging_root": rel(STAGING_ROOT),
        "products": [product.name for product in selected],
        "results": results,
        "ok": all(item.get("ok") or item.get("skipped") == "target_exists" for item in results),
    }
    if args.write:
        out_dir = ROOT / "qa_artifacts" / "release_validation"
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / "free-dev-staging.json"
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        data["written"] = rel(target)
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        for item in results:
            status = "skip" if item.get("skipped") else "ok" if item.get("ok") else "failed"
            print(f"{item['name']}: {status} -> {item['target']}")
        if args.write:
            print(f"wrote {data['written']}")
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
