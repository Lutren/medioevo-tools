from __future__ import annotations

import argparse
from zipfile import ZIP_DEFLATED, ZipFile

from _common import PRODUCTS, ROOT, add_common_args, collect_product_files, product_by_name, rel, validate_root_arg


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run or create free developer release packages.")
    add_common_args(parser)
    parser.add_argument("--product", choices=[p.name for p in PRODUCTS if p.lane == "free-dev"], action="append")
    parser.add_argument("--execute", action="store_true", help="actually write ZIP files")
    args = parser.parse_args()
    validate_root_arg(args)

    selected = [product_by_name(name) for name in args.product] if args.product else [p for p in PRODUCTS if p.lane == "free-dev"]
    out_dir = ROOT / "releases" / "free-dev"
    for product in selected:
        files, blocked, excluded = collect_product_files(product)
        print(f"{product.name}: {len(files)} files included, {len(blocked)} blocked, {len(excluded)} excluded")
        if blocked:
            for path, reason in blocked[:25]:
                print(f"  blocked {path} ({reason})")
            if args.execute:
                print("  skipped write because blocked items exist")
                continue
        if not args.execute:
            for path in files[:25]:
                print(f"  include {rel(path)}")
            continue
        out_dir.mkdir(parents=True, exist_ok=True)
        zip_path = out_dir / f"{product.name}.zip"
        with ZipFile(zip_path, "w", ZIP_DEFLATED) as zf:
            for path in files:
                zf.write(path, rel(path))
        print(f"wrote {rel(zip_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
