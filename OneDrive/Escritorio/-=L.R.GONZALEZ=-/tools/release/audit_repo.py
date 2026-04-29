from __future__ import annotations

import argparse
import os
from collections import Counter
from pathlib import Path

from _common import ROOT, add_common_args, is_denied, print_json, rel, validate_root_arg


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit workspace tree without modifying files.")
    add_common_args(parser)
    parser.add_argument("--json", action="store_true", help="print JSON instead of text")
    parser.add_argument("--include-denied", action="store_true", help="include archives, caches, builds, and vendor trees")
    args = parser.parse_args()
    validate_root_arg(args)

    file_count = 0
    dir_count = 0
    suffixes = Counter()
    top_stats: dict[str, dict[str, float | int | str]] = {}
    git_roots = []

    for base, dirs, files in os.walk(ROOT):
        base_path = ROOT if base == str(ROOT) else Path(base)
        if not args.include_denied:
            dirs[:] = [name for name in dirs if not is_denied(base_path / name)]
        dir_count += len(dirs)
        if ".git" in dirs:
            git_roots.append(rel(base_path))
        for filename in files:
            path = base_path / filename
            if not args.include_denied and is_denied(path):
                continue
            file_count += 1
            suffixes[path.suffix.lower() or "[no_ext]"] += 1
            try:
                size = path.stat().st_size
            except OSError:
                size = 0
            try:
                first = path.relative_to(ROOT).parts[0]
            except ValueError:
                first = "."
            row = top_stats.setdefault(first, {"path": first, "files": 0, "bytes": 0})
            row["files"] = int(row["files"]) + 1
            row["bytes"] = int(row["bytes"]) + size

    top = [
        {"path": str(row["path"]), "files": row["files"], "size_mb": round(int(row["bytes"]) / 1024 / 1024, 2)}
        for row in top_stats.values()
    ]
    top.sort(key=lambda row: row["path"].lower())

    data = {
        "root": str(ROOT),
        "files": file_count,
        "directories": dir_count,
        "top_level": top,
        "git_roots": sorted(git_roots),
        "top_extensions": suffixes.most_common(25),
    }
    if args.json:
        print_json(data)
    else:
        print(f"root: {ROOT}")
        print(f"files: {data['files']}")
        print(f"directories: {data['directories']}")
        print("top level:")
        for row in top:
            print(f"  {row['path']}: {row['files']} files, {row['size_mb']} MB")
        print("git roots:")
        for item in data["git_roots"][:80]:
            print(f"  {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
