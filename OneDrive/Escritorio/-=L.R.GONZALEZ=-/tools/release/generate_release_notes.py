from __future__ import annotations

import argparse
from datetime import date

from _common import PRODUCTS, ROOT, add_common_args, rel, validate_root_arg


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate draft release notes.")
    add_common_args(parser)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    validate_root_arg(args)

    lines = [
        f"# RELEASE_NOTES_DRAFT_{date.today().isoformat()}",
        "",
        "Status: draft. No publication implied.",
        "",
        "## Candidate Products",
        "",
    ]
    for product in PRODUCTS:
        lines.append(f"- {product.name}: {product.classification}; lane={product.lane}; {product.notes}")
    lines += [
        "",
        "## Required Evidence",
        "",
        "- secret scan",
        "- private game exclusion",
        "- product manifest",
        "- tests/build results",
        "- legal review where required",
    ]
    text = "\n".join(lines) + "\n"
    if args.write:
        out = ROOT / f"RELEASE_NOTES_DRAFT_{date.today().isoformat()}.md"
        out.write_text(text, encoding="utf-8")
        print(f"wrote {rel(out)}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
