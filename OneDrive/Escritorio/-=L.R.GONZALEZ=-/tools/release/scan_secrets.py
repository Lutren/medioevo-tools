from __future__ import annotations

import argparse
import re

from _common import (
    BINARY_SUFFIXES,
    add_common_args,
    is_denied,
    is_private_game,
    is_secret_named,
    iter_files,
    print_json,
    rel,
    validate_root_arg,
)


PATTERNS = [
    re.compile(r"(api[_-]?key|secret|token|password|passwd|private[_-]?key)\s*[:=]\s*[\"']?[^\s\"']{8,}", re.I),
    re.compile(r"bearer\s+[a-z0-9._-]+", re.I),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{16,}"),
]


def scan_text(path, max_bytes: int) -> list[str]:
    if path.suffix.lower() in BINARY_SUFFIXES or path.stat().st_size > max_bytes:
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    hits = []
    for pattern in PATTERNS:
        if pattern.search(text):
            hits.append(pattern.pattern)
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan for secret-like files and content without printing values.")
    add_common_args(parser)
    parser.add_argument("--max-bytes", type=int, default=300_000)
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--fail-on-findings", action="store_true")
    args = parser.parse_args()
    validate_root_arg(args)

    findings = []
    for path in iter_files(include_denied=False):
        reasons = []
        if is_private_game(path):
            continue
        if is_secret_named(path):
            reasons.append("secret-like filename")
        content_hits = scan_text(path, args.max_bytes)
        if content_hits:
            reasons.append("secret-like content markers")
        if reasons:
            findings.append({"path": rel(path), "reasons": sorted(set(reasons))})
        if len(findings) >= args.limit:
            break

    data = {"findings": findings, "count_reported": len(findings), "truncated_at": args.limit}
    if args.json:
        print_json(data)
    else:
        print(f"reported findings: {len(findings)}")
        for item in findings:
            print(f"- {item['path']} :: {', '.join(item['reasons'])}")
    return 1 if args.fail_on_findings and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
