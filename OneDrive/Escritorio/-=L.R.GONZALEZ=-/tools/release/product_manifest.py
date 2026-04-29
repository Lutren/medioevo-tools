from __future__ import annotations

import argparse
from pathlib import Path

from _common import ROOT, PRODUCTS, add_common_args, collect_product_files, print_json, rel, sha256_file, validate_root_arg


def product_summary(product, hash_files: bool = False) -> dict[str, object]:
    allowed_files, blocked_items, excluded_items = collect_product_files(product)
    files = []
    for path in allowed_files:
        row = {"path": rel(path), "bytes": path.stat().st_size}
        if hash_files:
            row["sha256"] = sha256_file(path)
        files.append(row)
    blocked = [{"path": path, "reason": reason} for path, reason in blocked_items]
    excluded = [{"path": path, "reason": reason} for path, reason in excluded_items]
    return {
        "name": product.name,
        "classification": product.classification,
        "lane": product.lane,
        "source": product.source,
        "notes": product.notes,
        "files": files,
        "blocked": blocked[:200],
        "excluded": excluded[:200],
        "file_count": len(files),
        "blocked_count": len(blocked),
        "excluded_count": len(excluded),
        "total_bytes": sum(item["bytes"] for item in files),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate product manifests from allowlisted products.")
    add_common_args(parser)
    parser.add_argument("--product", choices=[p.name for p in PRODUCTS], action="append")
    parser.add_argument("--hash", action="store_true")
    parser.add_argument("--write", action="store_true", help="write JSON manifests under release_manifests")
    args = parser.parse_args()
    validate_root_arg(args)

    selected = [p for p in PRODUCTS if not args.product or p.name in args.product]
    manifests = [product_summary(p, hash_files=args.hash) for p in selected]
    if args.write:
        out = ROOT / "release_manifests"
        out.mkdir(exist_ok=True)
        for manifest in manifests:
            target = out / f"{manifest['name']}.json"
            target.write_text(__import__("json").dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"wrote {rel(target)}")
    else:
        print_json(manifests)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
