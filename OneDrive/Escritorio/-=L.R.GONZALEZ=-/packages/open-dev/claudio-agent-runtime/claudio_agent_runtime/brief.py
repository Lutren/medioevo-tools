from __future__ import annotations

from pathlib import Path

from .doctor import run_doctor
from .memory_lite import memory_status
from .rphi_calibration import latest_calibration_status
from .rphi_budget import calculate_rphi_budget
from .task_board import list_tasks
from .witness_log import witness_status


def render_brief(root: str | Path = ".") -> str:
    doctor = run_doctor(root)
    memory = memory_status(root)
    tasks = list_tasks(root)
    witness = witness_status(root)
    budget = calculate_rphi_budget(root)
    calibration = latest_calibration_status(root)
    next_action = "Implement or run the next local dry-run P0 command with tests."
    if tasks["tasks"]:
        next_action = f"Close task {tasks['tasks'][0]['id']} with evidence."
    lines = [
        "# NEXT_SESSION_BRIEF CLAUDIO_AGENT_RUNTIME",
        "",
        "## Estado",
        f"state_root: {doctor['state_root']}",
        "external_channels: disabled",
        "ActionGate: local_dry_run",
        f"R_est: {budget['r_total']:.4f}",
        f"Phi_eff_est: {budget['phi_eff']:.4f}",
        f"Regimen: {budget['regime']}",
        f"ActionGate_suggestion: {budget['actiongate_suggestion']}",
        f"RPHI_calibration: {calibration.get('calibration_status', 'not_available') if calibration.get('exists') else 'not_available'}",
        "",
        "## Evidencia",
        f"memory_items: {memory['count']}",
        f"tasks: {tasks['count']}",
        f"witness_events: {witness['count']}",
        "secrets: presence-only reporting, values_printed=false",
        "",
        "## Pendientes reales",
        "- Keep P0 stdlib-only until tests and scans pass.",
        "- Keep Telegram/GitHub/Spotify/service install in REVIEW.",
        "",
        "## Proxima accion verificable",
        next_action,
        "",
        "## Segunda perdida",
        "Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.",
    ]
    return "\n".join(lines) + "\n"
