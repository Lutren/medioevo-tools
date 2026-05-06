from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from _common import add_common_args, iter_files, print_json, rel, sha256_file, validate_root_arg


def candidate_hash_files() -> list[Path]:
    by_size: dict[int, list[Path]] = defaultdict(list)
    for path in iter_files():
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size == 0 or size > 25 * 1024 * 1024:
            continue
        by_size[size].append(path)

    candidates: list[Path] = []
    for paths in by_size.values():
        if len(paths) > 1:
            candidates.extend(paths)
    return candidates


def main() -> int:
    parser = argparse.ArgumentParser(description="Find duplicate filenames or exact duplicate files.")
    add_common_args(parser)
    parser.add_argument("--mode", choices=["name", "hash"], default="name")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    validate_root_arg(args)

    groups = defaultdict(list)
    paths = iter_files() if args.mode == "name" else candidate_hash_files()
    for path in paths:
        if args.mode == "name":
            key = path.name.lower()
        else:
            try:
                key = f"{path.stat().st_size}:{sha256_file(path)}"
            except OSError:
                continue
        groups[key].append(rel(path))

    rows = []
    for key, paths in groups.items():
        if len(paths) > 1:
            rows.append({"key": key, "count": len(paths), "examples": paths[:5]})
    rows.sort(key=lambda row: row["count"], reverse=True)
    rows = rows[: args.limit]

    if args.json:
        print_json(rows)
    else:
        for row in rows:
            print(f"{row['count']:>5} {row['key']}")
            for example in row["examples"]:
                print(f"      {example}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
