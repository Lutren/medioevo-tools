"""Remote compute planning gates for DUAT simulation work."""

from __future__ import annotations

import json
from typing import Any

from .contracts import DUAT_REMOTE_COMPUTE_PLAN_SCHEMA, DUAT_REMOTE_RUN_SPEC_SCHEMA
from .smallville_lab import stable_hash


def _spec(
    *,
    provider: str,
    execution_mode: str,
    action_gate: str,
    command: str,
    network_required: bool,
    credentials_required: list[str],
    accelerator: str,
    status: str,
    reason: str,
    outputs: list[str],
    constraints: list[str],
) -> dict[str, Any]:
    payload = {
        "schema": DUAT_REMOTE_RUN_SPEC_SCHEMA,
        "provider": provider,
        "execution_mode": execution_mode,
        "action_gate": action_gate,
        "command": command,
        "network_required": network_required,
        "credentials_required": credentials_required,
        "accelerator": accelerator,
        "status": status,
        "reason": reason,
        "outputs": outputs,
        "constraints": constraints,
        "publication_gate": "BLOCK",
        "external_publication": False,
    }
    payload["spec_sha256"] = stable_hash(payload)
    return payload


def build_remote_compute_plan(
    *,
    scenario_id: str = "duat_smallville_city_v0_1",
    seed: str = "duat-smallville-v0-1",
) -> dict[str, Any]:
    """Return a non-executing plan for local and cloud-adjacent DUAT runs."""

    local_command = (
        "python -m geodia_social_observatory.cli smallville-duat "
        f"--seed {seed} --pretty --out reports/{scenario_id}-ledger.json"
    )
    specs = [
        _spec(
            provider="local_cpu",
            execution_mode="direct_local",
            action_gate="APPROVE_LOCAL",
            command=local_command,
            network_required=False,
            credentials_required=[],
            accelerator="CPU",
            status="READY_LOCAL",
            reason="Local deterministic CPU run uses synthetic fixtures only.",
            outputs=[f"reports/{scenario_id}-ledger.json"],
            constraints=["no_publication", "no_real_data_without_source_card"],
        ),
        _spec(
            provider="colab_notebook",
            execution_mode="manual_notebook_export",
            action_gate="REVIEW",
            command="open exported notebook manually; do not run background workers",
            network_required=True,
            credentials_required=["human_google_session_not_stored"],
            accelerator="GPU_OR_TPU_OPTIONAL_NOT_GUARANTEED",
            status="REVIEW_MANUAL_EXPORT",
            reason="Colab resources fluctuate and must not be used as unattended infrastructure.",
            outputs=[f"{scenario_id}-ledger.json", f"{scenario_id}-falsifier.json"],
            constraints=[
                "manual_runtime_only",
                "do_not_share_outputs_publicly",
                "do_not_mount_drive_with_private_workspace",
                "no_remote_control_shell",
            ],
        ),
        _spec(
            provider="kaggle_kernel",
            execution_mode="manual_kernel_export",
            action_gate="REVIEW",
            command="kaggle kernels push -p <exported_kernel_dir> --accelerator NvidiaTeslaT4 --timeout 3600",
            network_required=True,
            credentials_required=["KAGGLE_USERNAME_presence_only", "KAGGLE_KEY_presence_only"],
            accelerator="NvidiaTeslaT4_OR_AVAILABLE_REVIEW",
            status="REVIEW_CREDENTIALS_AND_QUOTA",
            reason="Kaggle requires account credentials and accelerator availability varies by quota and policy.",
            outputs=[f"{scenario_id}-ledger.json", f"{scenario_id}-falsifier.json"],
            constraints=[
                "private_kernel_only",
                "no_dataset_upload_without_manifest",
                "no_public_notebook",
                "no_private_paths",
            ],
        ),
        _spec(
            provider="simscale",
            execution_mode="api_or_workbench_review",
            action_gate="REVIEW",
            command="prepare physical microclimate/CFD run spec only after account/API/legal review",
            network_required=True,
            credentials_required=["SIMSCALE_API_KEY_presence_only"],
            accelerator="CLOUD_HPC_MANAGED_BY_PROVIDER",
            status="REVIEW_PHYSICS_ONLY",
            reason="SimScale is appropriate for physical CFD/FEA/thermal/microclimate jobs, not social cognition.",
            outputs=["physical_boundary_conditions.json", "provider_result_manifest.json"],
            constraints=[
                "physical_simulation_only",
                "no_social_agent_state_upload",
                "cost_and_license_review_required",
                "human_review_before_api_call",
            ],
        ),
    ]
    plan = {
        "schema": DUAT_REMOTE_COMPUTE_PLAN_SCHEMA,
        "scenario_id": scenario_id,
        "seed": seed,
        "policy": {
            "local_first": True,
            "external_execution_default": "REVIEW",
            "credentials_storage": "FORBIDDEN_IN_REPO",
            "publication_gate": "BLOCK",
        },
        "specs": specs,
        "falsifiers": falsify_remote_compute_plan(specs),
    }
    plan["plan_sha256"] = stable_hash(plan)
    return plan


def build_colab_kaggle_notebook(
    *,
    scenario_id: str = "duat_smallville_city_v0_1",
    seed: str = "duat-smallville-v0-1",
) -> dict[str, Any]:
    """Build a public-safe notebook template without executing remote code."""

    code = f"""from pathlib import Path
import json
import sys

# Upload only a sanitized copy of research/geodia-social-observatory.
# Do not mount private Drive folders and do not paste credentials.
sys.path.insert(0, "geodia-social-observatory")

from geodia_social_observatory.smallville_lab import falsify_smallville_run, run_smallville_duat_lab

ledger = run_smallville_duat_lab(seed={seed!r}, days=2, ticks_per_day=6, agent_count=25)
falsifier = falsify_smallville_run(ledger)

Path("{scenario_id}-ledger.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
Path("{scenario_id}-falsifier.json").write_text(json.dumps(falsifier, ensure_ascii=False, indent=2), encoding="utf-8")

print(json.dumps({{
    "status": "complete",
    "publication_gate": ledger["gates"]["publication_gate"],
    "falsifiers_passed": falsifier["passed"],
    "ledger_sha256": ledger["fingerprints"]["ledger_sha256"],
}}, indent=2))
"""
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "duat_policy": {
                "scenario_id": scenario_id,
                "publication_gate": "BLOCK",
                "credentials": "FORBIDDEN_IN_NOTEBOOK",
                "runtime": "manual_colab_or_kaggle_only",
            },
        },
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# DUAT Smallville Simulation Lab v0.1\\n",
                    "\\n",
                    "Manual Colab/Kaggle template. Synthetic data only. PublicationGate=BLOCK. ",
                    "No Drive mount with private workspace, no secrets, no public notebook sharing.\\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "PUBLICATION_GATE = 'BLOCK'\\n",
                    "EXTERNAL_PUBLICATION = False\\n",
                    "assert PUBLICATION_GATE == 'BLOCK'\\n",
                    "assert EXTERNAL_PUBLICATION is False\\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [line + "\\n" for line in code.splitlines()],
            },
        ],
    }
    notebook["metadata"]["duat_policy"]["notebook_sha256"] = stable_hash(notebook)
    return notebook


def falsify_remote_compute_plan(specs: list[dict[str, Any]]) -> dict[str, Any]:
    serialized = json.dumps(specs, ensure_ascii=False).lower()
    external_specs = [spec for spec in specs if spec["provider"] != "local_cpu"]
    checks = [
        {
            "name": "external_specs_not_auto_approved",
            "passed": all(spec["action_gate"] == "REVIEW" for spec in external_specs),
            "decision_if_failed": "BLOCK",
        },
        {
            "name": "local_cpu_available",
            "passed": any(spec["provider"] == "local_cpu" and spec["action_gate"] == "APPROVE_LOCAL" for spec in specs),
            "decision_if_failed": "REVIEW",
        },
        {
            "name": "no_secret_values",
            "passed": not any(marker in serialized for marker in ("sk-", "bearer ", "api_key=", "password=")),
            "decision_if_failed": "BLOCK",
        },
        {
            "name": "simscale_physics_only",
            "passed": all(
                spec["provider"] != "simscale" or "physical_simulation_only" in spec["constraints"]
                for spec in specs
            ),
            "decision_if_failed": "BLOCK",
        },
        {
            "name": "publication_blocked",
            "passed": all(spec["publication_gate"] == "BLOCK" and spec["external_publication"] is False for spec in specs),
            "decision_if_failed": "BLOCK",
        },
    ]
    return {
        "passed": all(check["passed"] for check in checks),
        "checks": checks,
        "publication_gate": "BLOCK",
    }


__all__ = ["build_colab_kaggle_notebook", "build_remote_compute_plan", "falsify_remote_compute_plan"]
