from __future__ import annotations

import argparse
import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from _common import ROOT, is_denied, is_private_game, is_secret_named, rel


REGISTRY_FILES = [
    "SOURCE_INTAKE_REGISTER.md",
    "source_intake_register.json",
    "PRODUCT_MAP.md",
    "VISIBILITY_MATRIX.md",
    "RISK_REGISTER.md",
    "DUPLICATES_AND_DEAD_CODE.md",
    "DELETE_CANDIDATES.md",
    "MIGRATION_MAP.md",
    "DELETED_OR_ARCHIVED.md",
    "docs/developer/TECHNOLOGY_IMPLEMENTATION_BACKLOG_2026-05-02.md",
    "docs/developer/DEPENDENCY_ADOPTION_GATE_2026-05-02.md",
    "docs/developer/CLAIM_FALSIFICATION_REGISTER_2026-05-02.md",
    "-=MEDIOEVO=-/-=LIBROS/claudio/CLAUDE.md",
    "-=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md",
    "-=MEDIOEVO=-/-=LIBROS/claudio/NEXT_SESSION_BRIEF.md",
]

DOC_GLOBS = [
    "docs/**/*.md",
    "-=MEDIOEVO=-/-=LIBROS/claudio/docs/**/*.md",
    "-=MEDIOEVO=-/-=LIBROS/claudio/tools/reports/**/*.md",
]


TECH_SIGNATURES = {
    "python_package": ["pyproject.toml", "setup.py", "requirements.txt"],
    "node_package": ["package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"],
    "rust_package": ["Cargo.toml", "Cargo.lock"],
    "dotnet_package": ["*.csproj", "*.sln"],
    "docs": ["README.md", "docs"],
    "license": ["LICENSE", "LICENSE.md", "COPYING"],
    "local_state": [".env", ".env.local", "settings.local.json"],
}


@dataclass
class Match:
    file: str
    line: int
    text: str
    kind: str


def normalize_token(value: str) -> str:
    return value.replace("\\", "/").lower().strip()


def path_tokens(raw_path: str, resolved: Path) -> list[str]:
    tokens = {
        normalize_token(raw_path),
        normalize_token(str(resolved)),
        normalize_token(resolved.as_posix()),
        normalize_token(resolved.name),
    }
    try:
        tokens.add(normalize_token(rel(resolved)))
    except OSError:
        pass
    parts = [part for part in normalize_token(resolved.as_posix()).split("/") if part]
    for depth in (2, 3, 4):
        if len(parts) >= depth:
            tokens.add("/".join(parts[-depth:]))
    return sorted(token for token in tokens if token)


def registry_paths() -> list[Path]:
    paths = [ROOT / name for name in REGISTRY_FILES]
    for pattern in DOC_GLOBS:
        paths.extend(ROOT.glob(pattern))
    unique: dict[str, Path] = {}
    for path in paths:
        if path.exists() and path.is_file():
            unique[str(path.resolve()).lower()] = path
    return sorted(unique.values(), key=lambda item: rel(item))


def line_matches(path: Path, tokens: Iterable[str]) -> list[Match]:
    matches: list[Match] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return matches
    token_list = sorted((token for token in tokens if token and len(token) >= 3), key=len, reverse=True)
    for index, line in enumerate(lines, start=1):
        lowered = normalize_token(line)
        for token in token_list:
            if token in lowered:
                kind = "exact_or_path" if "/" in token or "\\" in token else "name"
                safe_line = line.strip()[:220].encode("ascii", "backslashreplace").decode("ascii")
                matches.append(Match(rel(path), index, safe_line, kind))
                break
    return matches


def has_top_level(path: Path, pattern: str) -> bool:
    if "*" in pattern:
        return any(path.glob(pattern))
    return (path / pattern).exists()


def has_shallow_signature(path: Path, pattern: str) -> bool:
    if has_top_level(path, pattern):
        return True
    for glob_pattern in (f"*/{pattern}", f"*/*/{pattern}"):
        try:
            if any(path.glob(glob_pattern)):
                return True
        except OSError:
            return False
    return False


def inspect_tech(path: Path) -> dict[str, object]:
    result: dict[str, object] = {
        "exists": path.exists(),
        "is_dir": path.is_dir(),
        "is_file": path.is_file(),
        "signals": [],
        "top_level_entries": [],
        "git": None,
        "file_count_sample": 0,
        "stopped_at_sample_limit": False,
    }
    if not path.exists():
        return result

    if path.is_dir():
        try:
            result["top_level_entries"] = sorted(child.name for child in path.iterdir())[:80]
        except OSError:
            result["top_level_entries"] = []
        signals = []
        for name, patterns in TECH_SIGNATURES.items():
            if any(has_shallow_signature(path, pattern) for pattern in patterns):
                signals.append(name)
        result["signals"] = signals
        count = 0
        sample_limit = 5000
        for _, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in {".git", "node_modules", ".venv", "__pycache__"}]
            count += len(files)
            if count >= sample_limit:
                result["stopped_at_sample_limit"] = True
                break
        result["file_count_sample"] = min(count, sample_limit)
        result["git"] = git_status(path)
    else:
        result["signals"] = ["single_file"]
    return result


def git_status(path: Path) -> dict[str, object] | None:
    try:
        proc = subprocess.run(
            ["git", "-C", str(path), "status", "--short", "--branch", "--untracked-files=no"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    return {
        "status": lines,
        "dirty_tracked": any(line and not line.startswith("##") for line in lines),
    }


def classify_path(path: Path, matches: list[Match], tech: dict[str, object]) -> dict[str, object]:
    private = path.exists() and is_private_game(path)
    denied = path.exists() and is_denied(path)
    secret_named = path.exists() and is_secret_named(path)
    exact_matches = [m for m in matches if m.kind == "exact_or_path"]
    registered = bool(exact_matches)
    partial = bool(matches) and not registered
    signals = set(tech.get("signals", []))

    if private:
        decision = "PRIVATE_BOUNDARY_DO_NOT_COPY"
        required = ["VISIBILITY_MATRIX.md", "PRIVATE_GAME_BOUNDARY.md", "DELETE_CANDIDATES.md only if disposable"]
    elif denied or secret_named:
        decision = "DENIED_OR_SECRET_LIKE_DO_NOT_COPY"
        required = ["RISK_REGISTER.md", "DELETE_CANDIDATES.md if residue", "never publish from this path"]
    elif not registered:
        decision = "NEEDS_FICHA_BEFORE_USE"
        required = ["SOURCE_INTAKE_REGISTER.md for external/raw sources", "PRODUCT_MAP.md and VISIBILITY_MATRIX.md for repos/products"]
    elif {"python_package", "node_package", "rust_package"} & signals:
        decision = "REGISTERED_TECH_REVIEW_SELECTIVE_ABSORPTION"
        required = ["TECHNOLOGY_IMPLEMENTATION_BACKLOG", "DEPENDENCY_ADOPTION_GATE if external dependency", "tests or smoke evidence"]
    else:
        decision = "REGISTERED_CONTINUE_WITH_BOUNDARY"
        required = ["keep evidence current", "do not broaden scope without new ficha"]

    if partial:
        required.append("review partial/name-only matches before assuming registered")

    return {
        "registered": registered,
        "partial_match_only": partial,
        "private_game_path": private,
        "denied_path": denied,
        "secret_like_name": secret_named,
        "decision": decision,
        "required_registers": required,
    }


def ficha_template(raw_path: str, classification: dict[str, object], tech: dict[str, object]) -> str:
    signals = ", ".join(tech.get("signals", [])) or "UNKNOWN"
    registers = "; ".join(classification["required_registers"])
    return "\n".join(
        [
            "## Curador Ficha Template",
            "",
            f"- path: `{raw_path}`",
            "- status: `NEEDS_FICHA`",
            "- classification: `UNKNOWN_REVIEW_REQUIRED`",
            f"- tech_signals: `{signals}`",
            "- useful_tech: `CERTEZA: pending`",
            "- extraction_mode: `SELECTIVE_ABSORPTION_ONLY`",
            "- public_boundary: `do not publish until scan/path/claim/license pass`",
            "- private_boundary: `do not copy secrets, sessions, RPG/TCG, paid sources or raw private notes`",
            "- discard_rule: `if not useful, list in DELETE_CANDIDATES.md; do not delete directly`",
            f"- required_registers: `{registers}`",
            "- evidence: `command, hash, test, scan or line reference here`",
        ]
    )


def evaluate(raw_path: str) -> dict[str, object]:
    path = Path(raw_path)
    resolved = path if path.is_absolute() else ROOT / path
    try:
        resolved = resolved.resolve()
    except OSError:
        resolved = resolved.absolute()
    tokens = path_tokens(raw_path, resolved)
    matches: list[Match] = []
    for registry in registry_paths():
        matches.extend(line_matches(registry, tokens))
    tech = inspect_tech(resolved)
    classification = classify_path(resolved, matches, tech)
    return {
        "schema": "curador.preflight.v1",
        "path": raw_path,
        "resolved": str(resolved),
        "classification": classification,
        "tech": tech,
        "matches": [match.__dict__ for match in matches[:50]],
        "match_count": len(matches),
        "ficha_template": ficha_template(raw_path, classification, tech)
        if classification["decision"] == "NEEDS_FICHA_BEFORE_USE"
        else None,
    }


def render_markdown(results: list[dict[str, object]]) -> str:
    lines = ["# Curador Preflight", ""]
    for item in results:
        classification = item["classification"]
        tech = item["tech"]
        lines.extend(
            [
                f"## {item['path']}",
                "",
                f"- resolved: `{item['resolved']}`",
                f"- decision: `{classification['decision']}`",
                f"- registered: `{classification['registered']}`",
                f"- partial_match_only: `{classification['partial_match_only']}`",
                f"- tech_signals: `{', '.join(tech.get('signals', [])) or 'none'}`",
                f"- match_count: `{item['match_count']}`",
                "",
            ]
        )
        if item["matches"]:
            lines.append("### Matches")
            for match in item["matches"][:10]:
                lines.append(f"- `{match['file']}:{match['line']}` - {match['text']}")
            lines.append("")
        if item["ficha_template"]:
            lines.append(item["ficha_template"])
            lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Curador preflight for dirty repos, sources and residue.")
    parser.add_argument("--path", action="append", required=True, help="Path to verify. Repeat for multiple paths.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of markdown.")
    args = parser.parse_args()

    results = [evaluate(raw_path) for raw_path in args.path]
    if args.json:
        print(json.dumps({"ok": True, "results": results}, indent=2, ensure_ascii=True))
    else:
        print(render_markdown(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
