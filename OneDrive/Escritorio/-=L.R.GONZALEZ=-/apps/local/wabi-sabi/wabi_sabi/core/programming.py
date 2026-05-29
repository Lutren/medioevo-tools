from __future__ import annotations

import py_compile
from dataclasses import dataclass, field
from pathlib import Path
from textwrap import dedent

from wabi_sabi.core.gate import ActionGate
from wabi_sabi.core.patch_planner import build_file_patch_plan, resolve_workspace_text_target, sha256_text
from wabi_sabi.core.safe_executor import SafeExecutor

try:  # Canonical OSIT action gate from obsai-core (single source of truth).
    from obsai_core import evaluate_action as _obsai_evaluate_action
except Exception:  # pragma: no cover - degrade to the local keyword gate only.
    _obsai_evaluate_action = None


@dataclass(frozen=True)
class PatchResult:
    target: Path
    backup: Path | None
    diff: Path
    plan: Path | None
    rollback: Path | None
    execution: Path | None
    before_hash: str
    after_hash: str
    changed: bool
    verification: str
    gate: str = "APPROVE"
    gate_reasons: list[str] = field(default_factory=list)


def resolve_python_target(workspace: Path, target: str | Path) -> Path:
    return resolve_workspace_text_target(workspace, target, suffix=".py")


def gate_python_patch(*, intent: str, code: str, existed: bool) -> dict:
    """Evaluate a scoped Python patch with the local ActionGate and obsai-core
    ``evaluate_action`` (when importable) **before** anything is written.

    Returns the recorded gate verdict so it can be stored next to the before/after
    hashes. A hard-boundary intent (local BLOCK) or critical residue (obsai BLOCK)
    blocks the write; obsai REVIEW is recorded but does not block a scoped local apply.
    """
    local = ActionGate().evaluate_text(intent or "")
    reasons = [f"local:{reason}" for reason in local.reasons]
    obsai_status = "unavailable"
    theta: float | None = None
    residue: float | None = None
    if _obsai_evaluate_action is not None:
        action = {
            "action_type": "edit_file",
            "input": intent or "scoped_python_code_patch",
            "output": code[:1200],
            "risk": 0.45 if existed else 0.25,
            # SafeExecutor captures a rollback snapshot before writing, so the patch is reversible.
            "reversibility": 0.9,
            "self_check": {"summary": intent or "scoped_python_code_patch", "assumptions": ["scoped_single_file_python_patch"]},
        }
        result = _obsai_evaluate_action(action)
        obsai_status = str(result.get("status", "REVIEW"))
        theta = result.get("theta")
        residue = result.get("scores", {}).get("R")
        reasons.extend(f"obsai:{reason}" for reason in result.get("reasons", []))
    final_gate = "BLOCK" if local.gate == "BLOCK" or obsai_status == "BLOCK" else "APPROVE"
    return {
        "gate": final_gate,
        "reasons": list(dict.fromkeys(reasons)),
        "theta": theta,
        "residue": residue,
        "obsai_status": obsai_status,
        "local_gate": local.gate,
    }


def apply_python_patch(
    *,
    workspace: Path,
    runtime_root: Path,
    target: str | Path,
    code: str,
    intent: str = "",
) -> PatchResult:
    target_path = resolve_python_target(workspace, target)
    old_text = target_path.read_text(encoding="utf-8") if target_path.exists() else ""
    before_hash = sha256_text(old_text)
    new_text = build_new_python_text(old_text, code)
    after_hash = sha256_text(new_text)

    compile(new_text, str(target_path), "exec")

    # WS1.1: the scoped write passes through ActionGate/evaluate_action before executing,
    # and the gate verdict is carried into the plan + witness next to the content hashes.
    verdict = gate_python_patch(intent=intent, code=new_text, existed=target_path.exists())
    if verdict["gate"] == "BLOCK":
        raise ValueError("action_gate_blocked:" + (",".join(verdict["reasons"]) or "hard_boundary"))

    gate_reasons = [
        f"action_gate={verdict['gate']}",
        f"obsai_status={verdict['obsai_status']}",
        *verdict["reasons"],
    ]
    plan = build_file_patch_plan(
        workspace=workspace,
        target=target,
        content=new_text,
        summary="scoped_python_code_patch",
        suffix=".py",
        gate=verdict["gate"],
        extra_reasons=gate_reasons,
    )
    execution = SafeExecutor(workspace=workspace, runtime_root=runtime_root).execute(plan)
    if not execution.ok:
        raise ValueError(execution.error or execution.verification)
    if target_path.exists():
        py_compile.compile(str(target_path), doraise=True)

    return PatchResult(
        target=target_path,
        backup=execution.rollback_path,
        diff=execution.diff_path,
        plan=execution.plan_path,
        rollback=execution.rollback_path,
        execution=execution.execution_path,
        before_hash=before_hash,
        after_hash=after_hash,
        changed=execution.changed,
        verification=execution.verification,
        gate=verdict["gate"],
        gate_reasons=gate_reasons,
    )


def build_new_python_text(old_text: str, code: str) -> str:
    normalized_code = code.strip() + "\n"
    if normalized_code.strip() in old_text:
        return old_text
    if not old_text.strip():
        return normalized_code
    header = "\n\n# --- Wabi Sabi generated patch ---\n"
    return old_text.rstrip() + header + normalized_code


def code_for_prompt(prompt: str) -> tuple[str, str, list[str]]:
    lowered = prompt.lower()
    if "normalize_title" in lowered:
        return (
            normalize_title_function(),
            "Genere una funcion Python local normalize_title(text) para normalizar titulos.",
            ["El usuario pidio un helper pequeno y reversible en sandbox."],
        )
    if "archivo" in lowered and ("linea" in lowered or "lineas" in lowered or "línea" in lowered):
        return (
            file_summary_function(),
            "Genere una funcion Python local para leer un archivo y resumir sus lineas.",
            ["El usuario probablemente queria un helper reutilizable para archivos de texto."],
        )
    return (
        generic_module_template(prompt),
        "Genere un borrador de codigo local.",
        ["El pedido necesita revision humana o integracion dirigida para tocar codigo existente."],
    )


def file_summary_function() -> str:
    return dedent(
        '''
        from __future__ import annotations

        from pathlib import Path


        def summarize_file_lines(path: str | Path, preview_lines: int = 5) -> dict:
            """Read a text file and return a compact line summary."""
            file_path = Path(path)
            text = file_path.read_text(encoding="utf-8", errors="replace")
            lines = text.splitlines()
            return {
                "path": str(file_path),
                "line_count": len(lines),
                "empty_lines": sum(1 for line in lines if not line.strip()),
                "first_lines": lines[:preview_lines],
                "last_lines": lines[-preview_lines:] if preview_lines else [],
            }
        '''
    ).lstrip()


def normalize_title_function() -> str:
    return dedent(
        '''
        from __future__ import annotations


        def normalize_title(text: str) -> str:
            """Collapse extra whitespace and return title case text."""
            return " ".join(str(text).split()).title()
        '''
    ).lstrip()


def generic_module_template(prompt: str) -> str:
    escaped = prompt.replace('"""', '\\"\\"\\"')
    return dedent(
        f'''
        """Generated Wabi Sabi code draft.

        Original request:
        {escaped}
        """


        def run() -> str:
            return "TODO: complete this local implementation after selecting a target file."


        if __name__ == "__main__":
            print(run())
        '''
    ).lstrip()
