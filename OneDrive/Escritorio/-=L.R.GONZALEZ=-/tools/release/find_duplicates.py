from __future__ import annotations

import argparse
from collections import defaultdict

from _common import add_common_args, iter_files, print_json, rel, sha256_file, validate_root_arg


def main() -> int:
    parser = argparse.ArgumentParser(description="Find duplicate filenames or exact duplicate files.")
    add_common_args(parser)
    parser.add_argument("--mode", choices=["name", "hash"], default="name")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    validate_root_arg(args)

    groups = defaultdict(list)
    for path in iter_files():
        if args.mode == "name":
            key = path.name.lower()
        else:
            if path.stat().st_size == 0 or path.stat().st_size > 25 * 1024 * 1024:
                continue
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
