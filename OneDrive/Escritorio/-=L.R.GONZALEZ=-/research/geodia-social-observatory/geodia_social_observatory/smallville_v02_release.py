"""Artifact writer for DUAT Smallville Simulation Lab v0.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .intervention_engine import build_baseline_intervention_pair
from .metrics_v0_2 import build_metrics_v0_2, falsify_v0_2
from .replay_verifier import verify_replay
from .signal_source_pack import DEFAULT_SEED
from .smallville_lab import stable_hash


ARTIFACT_NAMES = {
    "pack": "duat-smallville-signal-pack-v0-2.json",
    "baseline": "duat-smallville-baseline-run-v0-2-ledger.json",
    "intervention": "duat-smallville-intervention-run-v0-2-ledger.json",
    "delta": "duat-smallville-intervention-delta-v0-2.json",
    "replay": "duat-smallville-replay-verification-v0-2.json",
    "metrics": "duat-smallville-metrics-v0-2.json",
    "falsifier": "duat-smallville-sim-lab-v0-2-falsifier.json",
    "report": "DUAT_SMALLVILLE_SIM_LAB_v0_2_REPORT.md",
}


def workspace_root() -> Path:
    return Path(__file__).resolve().parents[3]


def default_artifact_dir() -> Path:
    return workspace_root() / "qa_artifacts" / "release_validation"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def render_report(
    *,
    pack: dict[str, Any],
    baseline: dict[str, Any],
    intervention: dict[str, Any],
    delta: dict[str, Any],
    replay: dict[str, Any],
    metrics: dict[str, Any],
    falsifier: dict[str, Any],
    artifact_paths: dict[str, str],
) -> str:
    failed = falsifier.get("failed", [])
    return (
        "# DUAT_SMALLVILLE_SIM_LAB_v0_2_REPORT\n\n"
        "## ESTADO\n"
        "ActionGate: APPROVE_LOCAL_CPU_TESTS_DOCS_SYNTHETIC_DATA\n"
        "RemoteComputeGate: REVIEW_COLAB_KAGGLE_SIMSCALE\n"
        "PublicationGate: BLOCK\n"
        "Mode: LOCAL_SYNTHETIC_CPU_ONLY\n\n"
        "## Que se implemento\n"
        "- SignalSourcePack sintetico local para weather, geophysics, social_pressure, infrastructure y resource_availability.\n"
        "- Canales ambientales calibrados con latency, bandwidth, calibration, noise, missingness y contradiction.\n"
        "- Intervencion contrafactual `weather_shock` con baseline, intervencion y delta hash-linked.\n"
        "- Replay verifier determinista y hash-chain.\n"
        "- Metricas R/Phi_eff/J_c y falsadores v0.2.\n\n"
        "## Que NO se implemento\n"
        "- No se aumentaron agentes.\n"
        "- No se agregaron graficos ni UI visual.\n"
        "- No se usaron red, cloud, providers, credenciales, Colab, Kaggle ni SimScale.\n"
        "- No hay datos reales ni prediccion social real.\n\n"
        "## Baseline vs intervention\n"
        f"- Baseline hash: `{baseline['fingerprints']['ledger_sha256']}`\n"
        f"- Intervention hash: `{intervention['fingerprints']['ledger_sha256']}`\n"
        f"- Delta R mean: `{delta['intervention_delta']['delta_R_mean']}`\n"
        f"- Delta Phi_eff mean: `{delta['intervention_delta']['delta_Phi_eff_mean']}`\n"
        f"- Changed agents: `{delta['intervention_delta']['changed_agent_count']}`\n"
        f"- Changed plans: `{delta['intervention_delta']['changed_plan_count']}`\n\n"
        "## Metricas R/Phi_eff/J_c\n"
        f"- R_env_mean: `{metrics['R']['R_env_mean']}`\n"
        f"- R_social_mean: `{metrics['R']['R_social_mean']}`\n"
        f"- R_contradiction_max: `{metrics['R']['R_contradiction_max']}`\n"
        f"- fusion_R_mean: `{metrics['R']['fusion_R_mean']}`\n"
        f"- J_c_proximity_max: `{metrics['R']['J_c_proximity_max']}`\n"
        f"- Phi_eff mean/min/max: `{metrics['Phi_eff']['mean']}` / `{metrics['Phi_eff']['min']}` / `{metrics['Phi_eff']['max']}`\n"
        f"- Gates: `{metrics['gates']}`\n\n"
        "## Falsadores\n"
        f"- Passed: `{falsifier['passed']}`\n"
        f"- Failed: `{failed}`\n"
        "- Bias boundary: AUDITABLE_NOT_ABSENT. No se declara ausencia absoluta de sesgos.\n\n"
        "## Replay verification\n"
        f"- Status: `{replay['status']}`\n"
        f"- Hash-chain valid: `{replay['hash_chain_valid']}`\n"
        f"- Replay verified: `{replay['replay_verified']}`\n\n"
        "## Boundary / no-real-data check\n"
        f"- uses_real_data: `{pack['boundary']['uses_real_data']}`\n"
        f"- uses_network: `{pack['boundary']['uses_network']}`\n"
        f"- uses_credentials: `{pack['boundary']['uses_credentials']}`\n"
        f"- publication_gate: `{pack['boundary']['publication_gate']}`\n\n"
        "## Tests ejecutados\n"
        "- Ver `TEST_REPORT.md` para resultados ejecutados en este run.\n\n"
        "## Incognitas\n"
        "- Remote compute permanece REVIEW y no se ejecuto.\n"
        "- Datos reales, sensores y calibracion externa quedan fuera del run.\n\n"
        "## Next action\n"
        "Revisar reporte v0.2; si PASS, preparar v0.3 UI panel Simulation Evidence / Active Contracts sin abrir compute remoto.\n\n"
        "## Artifacts\n"
        + "\n".join(f"- {name}: `{path}`" for name, path in artifact_paths.items())
        + "\n"
    )


def build_release_artifacts(
    *,
    out_dir: str | Path | None = None,
    seed: int = DEFAULT_SEED,
    ticks: int = 1440,
    intervention_name: str = "weather_shock",
) -> dict[str, Any]:
    artifact_dir = Path(out_dir) if out_dir is not None else default_artifact_dir()
    artifact_dir.mkdir(parents=True, exist_ok=True)
    pair = build_baseline_intervention_pair(seed=seed, ticks=ticks, intervention_name=intervention_name)
    replay = verify_replay(pair["baseline"], pair["pack"])
    falsifier = falsify_v0_2(pair["pack"], pair["baseline"], pair["intervention"], pair["delta"])
    metrics = build_metrics_v0_2(
        seed=seed,
        pack=pair["pack"],
        baseline=pair["baseline"],
        intervention=pair["intervention"],
        delta=pair["delta"],
        replay=replay,
        falsifier=falsifier,
    )
    payloads = {
        "pack": pair["pack"],
        "baseline": pair["baseline"],
        "intervention": pair["intervention"],
        "delta": pair["delta"],
        "replay": replay,
        "metrics": metrics,
        "falsifier": falsifier,
    }
    paths: dict[str, str] = {}
    for key, payload in payloads.items():
        path = artifact_dir / ARTIFACT_NAMES[key]
        write_json(path, payload)
        paths[key] = str(path)
    report_path = artifact_dir / ARTIFACT_NAMES["report"]
    report_path.write_text(
        render_report(
            pack=pair["pack"],
            baseline=pair["baseline"],
            intervention=pair["intervention"],
            delta=pair["delta"],
            replay=replay,
            metrics=metrics,
            falsifier=falsifier,
            artifact_paths=paths,
        ),
        encoding="utf-8",
    )
    paths["report"] = str(report_path)
    manifest = {
        "run_id": "DUAT-SMALLVILLE-SCI-SIM-v0-2-20260517",
        "seed": seed,
        "ticks": ticks,
        "intervention": intervention_name,
        "artifacts": paths,
        "hashes": {
            key: stable_hash(json.loads(Path(path).read_text(encoding="utf-8")))
            if path.endswith(".json")
            else stable_hash(Path(path).read_text(encoding="utf-8"))
            for key, path in paths.items()
        },
        "publication_gate": "BLOCK",
        "remote_compute_gate": "REVIEW_COLAB_KAGGLE_SIMSCALE",
    }
    return manifest


__all__ = ["ARTIFACT_NAMES", "build_release_artifacts", "default_artifact_dir", "workspace_root"]
