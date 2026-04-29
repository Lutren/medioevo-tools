from __future__ import annotations

import argparse

from _common import add_common_args, iter_files, print_json, rel, validate_root_arg


def main() -> int:
    parser = argparse.ArgumentParser(description="Find large files without modifying anything.")
    add_common_args(parser)
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--min-mb", type=float, default=25.0)
    parser.add_argument("--include-denied", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    validate_root_arg(args)

    rows = []
    for path in iter_files(include_denied=args.include_denied):
        size = path.stat().st_size
        mb = size / 1024 / 1024
        if mb >= args.min_mb:
            rows.append({"path": rel(path), "mb": round(mb, 2)})
    rows.sort(key=lambda row: row["mb"], reverse=True)
    rows = rows[: args.limit]

    if args.json:
        print_json(rows)
    else:
        for row in rows:
            print(f"{row['mb']:>10} MB  {row['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
