from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .memory_lite import memory_status
from .rphi_calibration import latest_calibration_status
from .rphi_budget import calculate_rphi_budget
from .task_board import list_tasks
from .witness_log import witness_status


SECRET_ENV_NAMES = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "DEEPSEEK_API_KEY",
    "GROK_API_KEY",
    "GITHUB_TOKEN",
    "TELEGRAM_BOT_TOKEN",
    "SPOTIFY_CLIENT_SECRET",
]


def run_doctor(state_root: str | Path = ".") -> dict[str, Any]:
    root = Path(state_root)
    config_root = root / "config"
    skills_root = root / "skills"
    permissions_manifest = config_root / "permissions.yaml"
    runtime_config = config_root / "runtime.yaml"
    secret_presence = {name: bool(os.environ.get(name)) for name in SECRET_ENV_NAMES}
    return {
        "schema_version": "claudio.doctor.v0.1",
        "state_root": str(root),
        "state_root_exists": root.exists(),
        "permissions_manifest": {
            "path": str(permissions_manifest),
            "exists": permissions_manifest.exists(),
        },
        "runtime_config": {
            "path": str(runtime_config),
            "exists": runtime_config.exists(),
        },
        "action_gate": {"available": True, "mode": "local_dry_run"},
        "skills_registry": {
            "path": str(skills_root),
            "exists": skills_root.exists(),
        },
        "memory_lite": memory_status(root),
        "task_board": list_tasks(root),
        "witness_log": witness_status(root),
        "rphi_budget": calculate_rphi_budget(root),
        "rphi_calibration": latest_calibration_status(root),
        "secrets": {
            "presence_only": True,
            "values_printed": False,
            "env": secret_presence,
        },
        "external_channels": {
            "telegram": "disabled",
            "github_write": "disabled",
            "spotify": "disabled",
        },
    }
