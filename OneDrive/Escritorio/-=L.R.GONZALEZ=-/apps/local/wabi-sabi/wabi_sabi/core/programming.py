from __future__ import annotations

import difflib
import hashlib
import py_compile
from dataclasses import dataclass
from pathlib import Path

from wabi_sabi.core.tools import stamp


SENSITIVE_PATH_PARTS = {
    ".git",
    ".claw",
    ".claude",
    ".wrangler",
    ".env",
    ".venv",
    ".venv_api",
    "node_modules",
    "runtime",
    "releases",
    "release",
    "dist",
    "build",
    "target",
    "game-private",
    "metaevo-tcg",
    "tcg",
    "game_bridge",
}


@dataclass(frozen=True)
class PatchResult:
    target: Path
    backup: Path | None
    diff: Path
    before_hash: str
    after_hash: str
    changed: bool
    verification: str


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def resolve_python_target(workspace: Path, target: str | Path) -> Path:
    workspace = workspace.resolve()
    raw = Path(target)
    candidate = raw.resolve() if raw.is_absolute() else (workspace / raw).resolve()
    if candidate != workspace and workspace not in candidate.parents:
        raise ValueError(f"target_outside_workspace:{candidate}")
    lowered_parts = {part.lower() for part in candidate.parts}
    blocked = sorted(SENSITIVE_PATH_PARTS.intersection(lowered_parts))
    if blocked:
        raise ValueError("target_path_blocked:" + ",".join(blocked))
    if candidate.suffix.lower() != ".py":
        raise ValueError("only_python_targets_supported")
    return candidate


def apply_python_patch(
    *,
    workspace: Path,
    runtime_root: Path,
    target: str | Path,
    code: str,
) -> PatchResult:
    target_path = resolve_python_target(workspace, target)
    old_text = target_path.read_text(encoding="utf-8") if target_path.exists() else ""
    before_hash = sha256_text(old_text)
    new_text = build_new_python_text(old_text, code)
    after_hash = sha256_text(new_text)
    changed = new_text != old_text

    compile(new_text, str(target_path), "exec")

    backup_path: Path | None = None
    if changed:
        backup_dir = runtime_root / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        safe_rel = "_".join(part for part in target_path.relative_to(workspace).parts)
        if old_text:
            backup_path = backup_dir / f"{safe_rel}_{stamp()}.bak"
            backup_path.write_text(old_text, encoding="utf-8")
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(new_text, encoding="utf-8")
        py_compile.compile(str(target_path), doraise=True)

    diff_dir = runtime_root / "outputs"
    diff_dir.mkdir(parents=True, exist_ok=True)
    diff_path = diff_dir / f"programmer_patch_{stamp()}.diff"
    rel = str(target_path.relative_to(workspace))
    diff_text = "".join(
        difflib.unified_diff(
            old_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=f"a/{rel}",
            tofile=f"b/{rel}",
        )
    )
    diff_path.write_text(diff_text or f"# no textual change for {rel}\n", encoding="utf-8")

    return PatchResult(
        target=target_path,
        backup=backup_path,
        diff=diff_path,
        before_hash=before_hash,
        after_hash=after_hash,
        changed=changed,
        verification="py_compile_passed",
    )


def build_new_python_text(old_text: str, code: str) -> str:
    normalized_code = code.strip() + "\n"
    if normalized_code.strip() in old_text:
        return old_text
    if not old_text.strip():
        return normalized_code
    header = "\n\n# --- Wabi Sabi generated patch ---\n"
    return old_text.rstrip() + header + normalized_code
