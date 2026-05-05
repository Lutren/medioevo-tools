from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INBOX = ROOT / "COMMS" / "inbox" / "claudio-local-agent.jsonl"
DEFAULT_EXAMPLES = (
    ROOT
    / "qa_artifacts"
    / "release_validation"
    / "seto-observacionismo-decision-examples-2026-05-05.jsonl"
)

SOURCE_HASHES = {
    "Downloads/sensorium_inversion_lab.py": "DF5105E2E46D09C31AA22F6CBB3931EE1C5FF0963A666F247ECADF9FFFA346B2",
    "Downloads/TUIP_SIGMA_R2_1_PRAGMATIC_CANON.md": "62C6F2E56977F3AC83AF30DA115ACD44338D800599A2BA30F4DAC633E14DA04F",
    "Downloads/tuip_sigma_core.py": "C5380DE6BF94392D4120653AFF55BC70FB67BEE035065C90BF06AE77B2F974F1",
    "Downloads/observacionismo_v8_1_addons.txt": "2E9D8A6F6317789AD08D71CC5FF9821275898DE8C1ED90DAD4CB2048AFBD6C45",
}

CHANNELS = [
    "photon",
    "electric",
    "magnetic",
    "gravity",
    "thermal",
    "acoustic",
    "chemical",
    "temporal_phase",
]

OBSERVER_PROFILES = {
    "human_visual": {
        "photon": 0.95,
        "electric": 0.10,
        "magnetic": 0.08,
        "gravity": 0.03,
        "thermal": 0.35,
        "acoustic": 0.60,
        "chemical": 0.40,
        "temporal_phase": 0.18,
    },
    "instrument_balanced": {
        "photon": 0.70,
        "electric": 0.70,
        "magnetic": 0.70,
        "gravity": 0.55,
        "thermal": 0.70,
        "acoustic": 0.70,
        "chemical": 0.65,
        "temporal_phase": 0.60,
    },
    "dark_observer": {
        "photon": 0.05,
        "electric": 0.70,
        "magnetic": 0.80,
        "gravity": 0.90,
        "thermal": 0.55,
        "acoustic": 0.30,
        "chemical": 0.45,
        "temporal_phase": 0.75,
    },
    "phase_observer": {
        "photon": 0.30,
        "electric": 0.55,
        "magnetic": 0.60,
        "gravity": 0.40,
        "thermal": 0.45,
        "acoustic": 0.35,
        "chemical": 0.35,
        "temporal_phase": 0.95,
    },
    "low_bandwidth_human": {
        "photon": 0.65,
        "electric": 0.04,
        "magnetic": 0.04,
        "gravity": 0.02,
        "thermal": 0.20,
        "acoustic": 0.35,
        "chemical": 0.20,
        "temporal_phase": 0.05,
    },
}

BLOCK_PATTERNS = {
    "medical_claim": re.compile(r"\b(cancer|diagnostico|diagnóstico|tratamiento medico|tratamiento médico|cura)\b", re.I),
    "strong_physics_claim": re.compile(r"\b(antigravedad real|nueva fisica|nueva física|energia libre|energía libre|prueba fisica|prueba física)\b", re.I),
    "social_prediction": re.compile(r"\b(predecir elecciones|prediccion social real|predicción social real|manipular masas)\b", re.I),
    "publication_or_external_action": re.compile(r"\b(publicar|subir a internet|deploy|push|gumroad|linkedin|github sponsors)\b", re.I),
    "secret_like": re.compile(r"\b(api[_-]?key|token|password|credential|credencial|secret(?!\s+scan))\b", re.I),
}

RISK_PATTERNS = {
    "raw_theory": re.compile(r"\b(teoria|teoría|canon|observacionismo|sigma|tuip|psi)\b", re.I),
    "delete_move": re.compile(r"\b(borrar|eliminar|mover|archivar|delete|remove)\b", re.I),
    "agent_autonomy": re.compile(r"\b(autonomo|autónomo|agente local|claudio|wabi|executor|patch)\b", re.I),
    "private_boundary": re.compile(r"\b(privado|rpg|tcg|familia|sobrinos|padres)\b", re.I),
    "uncertainty": re.compile(r"\b(creo|quizas|quizás|infer|hipotesis|hipótesis|incognita|incógnita)\b", re.I),
}


@dataclass(frozen=True)
class ProfileObservation:
    profile: str
    clarity: float
    visual_dependency: float
    channel_coverage: float
    cross_channel_coherence: float
    signal: float


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text_inputs(paths: list[Path], inline_text: str | None) -> tuple[str, dict[str, str], list[str]]:
    chunks: list[str] = []
    hashes: dict[str, str] = dict(SOURCE_HASHES)
    errors: list[str] = []
    if inline_text:
        chunks.append(inline_text)
        hashes["inline_text"] = hashlib.sha256(inline_text.encode("utf-8")).hexdigest()
    for path in paths:
        try:
            data = path.read_text(encoding="utf-8", errors="replace")
        except FileNotFoundError:
            errors.append(f"missing input: {rel(path)}")
            continue
        chunks.append(data)
        hashes[rel(path)] = sha256_file(path)
    return "\n".join(chunks), hashes, errors


def load_jsonl_count(path: Path) -> int:
    if not path.exists():
        return 0
    count = 0
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                json.loads(line)
                count += 1
    return count


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return min(high, max(low, value))


def keyword_density(text: str, pattern: re.Pattern[str]) -> float:
    if not text.strip():
        return 0.0
    hits = len(pattern.findall(text))
    words = max(1, len(re.findall(r"\w+", text)))
    return clamp(hits / max(1.0, words / 80.0))


def extract_flags(text: str) -> tuple[list[str], list[str]]:
    blocked = [name for name, pattern in BLOCK_PATTERNS.items() if pattern.search(text)]
    risks = [name for name, pattern in RISK_PATTERNS.items() if pattern.search(text)]
    return sorted(blocked), sorted(risks)


def estimate_evidence_score(text: str, examples_count: int) -> float:
    evidence_terms = len(
        re.findall(
            r"\b(hash|sha256|evidencia|test|smoke|schema|json|witness|falsador|gate|contrato)\b",
            text,
            re.I,
        )
    )
    length_bonus = min(0.25, len(text) / 12000.0)
    example_bonus = min(0.20, examples_count / 20.0)
    return clamp(0.18 + (evidence_terms * 0.018) + length_bonus + example_bonus)


def phi_eff(R: float, J_c: float = 1.0, nu: float = 1.0) -> float:
    if R >= J_c:
        return 0.0
    if R <= 0:
        return 1.0
    return clamp(math.exp(-nu * R / (J_c - R)))


def observationist_pass(text: str, examples_count: int, input_errors: list[str]) -> dict[str, Any]:
    blocked_flags, risk_flags = extract_flags(text)
    evidence_score = estimate_evidence_score(text, examples_count)
    ambiguity = keyword_density(text, RISK_PATTERNS["uncertainty"])
    risk_score = clamp((0.16 * len(risk_flags)) + (0.22 * len(blocked_flags)) + ambiguity + (0.18 if input_errors else 0.0))
    R = clamp((1.0 - evidence_score) * 0.45 + risk_score * 0.55)
    J_c = 1.0
    phi = phi_eff(R, J_c=J_c, nu=1.0)

    reasons: list[str] = []
    if input_errors:
        reasons.extend(input_errors)
    if blocked_flags:
        reasons.append(f"blocked flags detected: {', '.join(blocked_flags)}")
    if evidence_score < 0.45:
        reasons.append("evidence score below operational threshold")
    if risk_flags:
        reasons.append(f"risk flags detected: {', '.join(risk_flags)}")
    if phi <= 0.60:
        reasons.append("Phi_eff at or below review threshold")

    if blocked_flags:
        gate = "BLOCK"
    elif phi <= 0.60 or risk_score >= 0.45 or evidence_score < 0.45:
        gate = "REVIEW"
    else:
        gate = "APPROVE"

    return {
        "R": round(R, 6),
        "J_c": J_c,
        "Phi_eff": round(phi, 6),
        "evidence_score": round(evidence_score, 6),
        "risk_score": round(risk_score, 6),
        "blocked_flags": blocked_flags,
        "risk_flags": risk_flags,
        "gate": gate,
        "reasons": reasons or ["local operational evidence is coherent enough for current gate"],
    }


def channel_signal(text: str) -> dict[str, float]:
    lower = text.lower()
    densities = {
        "photon": len(re.findall(r"\b(ver|visual|imagen|luz|foto|pixel|color)\b", lower)),
        "electric": len(re.findall(r"\b(electric|electron|volt|circuit|señal|senal)\b", lower)),
        "magnetic": len(re.findall(r"\b(magnetic|magnet|campo)\b", lower)),
        "gravity": len(re.findall(r"\b(gravity|gravedad|peso|masa)\b", lower)),
        "thermal": len(re.findall(r"\b(thermal|termico|térmico|calor|temperatura)\b", lower)),
        "acoustic": len(re.findall(r"\b(acoustic|audio|sonido|voz)\b", lower)),
        "chemical": len(re.findall(r"\b(chemical|quimic|químic|olor|sabor)\b", lower)),
        "temporal_phase": len(re.findall(r"\b(tiempo|fase|ritmo|secuencia|latencia|loop)\b", lower)),
    }
    total = sum(densities.values())
    if total == 0:
        return {channel: 1.0 / len(CHANNELS) for channel in CHANNELS}
    return {channel: clamp((densities[channel] + 1.0) / (total + len(CHANNELS))) for channel in CHANNELS}


def profile_observe(profile: str, weights: dict[str, float], signal_by_channel: dict[str, float]) -> ProfileObservation:
    weighted = {channel: weights[channel] * signal_by_channel[channel] for channel in CHANNELS}
    signal = sum(weighted.values())
    clarity = clamp(signal / max(0.01, sum(signal_by_channel.values())))
    visual_dependency = clamp(weighted["photon"] / max(0.001, signal))
    active_channels = sum(1 for channel in CHANNELS if weighted[channel] >= 0.035)
    coverage = clamp(active_channels / len(CHANNELS))
    values = list(weighted.values())
    mean_value = sum(values) / len(values)
    variance = sum((value - mean_value) ** 2 for value in values) / len(values)
    coherence = clamp(1.0 - math.sqrt(variance) * 4.0)
    return ProfileObservation(
        profile=profile,
        clarity=round(clarity, 6),
        visual_dependency=round(visual_dependency, 6),
        channel_coverage=round(coverage, 6),
        cross_channel_coherence=round(coherence, 6),
        signal=round(signal, 6),
    )


def inverse_observationist_pass(text: str) -> dict[str, Any]:
    signal_by_channel = channel_signal(text)
    observations = [
        profile_observe(profile, weights, signal_by_channel)
        for profile, weights in OBSERVER_PROFILES.items()
    ]
    baseline = observations[0]
    signature_distances: dict[str, float] = {}
    for obs in observations[1:]:
        distance = math.sqrt(
            (obs.clarity - baseline.clarity) ** 2
            + (obs.visual_dependency - baseline.visual_dependency) ** 2
            + (obs.channel_coverage - baseline.channel_coverage) ** 2
            + (obs.cross_channel_coherence - baseline.cross_channel_coherence) ** 2
        )
        signature_distances[f"{baseline.profile}->{obs.profile}"] = round(distance, 6)

    mean_distance = sum(signature_distances.values()) / max(1, len(signature_distances))
    stability_score = clamp(1.0 - mean_distance)
    mean_visual = sum(obs.visual_dependency for obs in observations) / len(observations)
    mean_coverage = sum(obs.channel_coverage for obs in observations) / len(observations)
    mean_coherence = sum(obs.cross_channel_coherence for obs in observations) / len(observations)
    invariant_score = clamp((stability_score * 0.45) + (mean_coverage * 0.25) + (mean_coherence * 0.30))

    hidden_bias_flags: list[str] = []
    if mean_visual >= 0.55:
        hidden_bias_flags.append("visual_channel_overweight")
    if mean_coverage < 0.55:
        hidden_bias_flags.append("low_channel_coverage")
    if stability_score < 0.55:
        hidden_bias_flags.append("observer_profile_instability")
    if invariant_score < 0.60:
        hidden_bias_flags.append("weak_cross_observer_invariant")

    if invariant_score >= 0.76 and not hidden_bias_flags:
        conclusion_state = "CERTEZA"
    elif invariant_score >= 0.58:
        conclusion_state = "INFERENCIA"
    else:
        conclusion_state = "INCOGNITA"

    return {
        "profiles": [obs.profile for obs in observations],
        "channels": CHANNELS,
        "channel_signal": {channel: round(value, 6) for channel, value in signal_by_channel.items()},
        "observations": [asdict(obs) for obs in observations],
        "signature_distances": signature_distances,
        "stability_score": round(stability_score, 6),
        "visual_dependency": round(mean_visual, 6),
        "invariant_score": round(invariant_score, 6),
        "hidden_bias_flags": hidden_bias_flags,
        "conclusion_state": conclusion_state,
    }


def combine_state(observation: dict[str, Any], inverse: dict[str, Any]) -> tuple[str, str, str]:
    if observation["gate"] == "BLOCK":
        return "BLOCK", "BLOQUEADO", "Blocked by ActionGate boundary flags."
    if inverse["conclusion_state"] == "INCOGNITA" or observation["gate"] == "REVIEW":
        return "REVIEW", "INFERENCIA", "Operationally useful but still requires review before autonomous write action."
    if observation["gate"] == "APPROVE" and inverse["conclusion_state"] == "CERTEZA":
        return "PASS", "CERTEZA", "Local operational pattern is stable across gates and observers."
    return "REVIEW", "INFERENCIA", "Pattern is coherent but not strong enough for autonomous execution."


def build_result(paths: list[Path], inline_text: str | None) -> dict[str, Any]:
    text, source_hashes, input_errors = read_text_inputs(paths, inline_text)
    examples_count = load_jsonl_count(DEFAULT_EXAMPLES)
    if DEFAULT_EXAMPLES.exists():
        source_hashes[rel(DEFAULT_EXAMPLES)] = sha256_file(DEFAULT_EXAMPLES)
    observation = observationist_pass(text, examples_count, input_errors)
    inverse = inverse_observationist_pass(text)
    status, claim_state, recommendation = combine_state(observation, inverse)

    falsifiers = [
        "Source hashes do not match the curated intake register.",
        "Observer-profile perturbation changes conclusion from CERTEZA/INFERENCIA to INCOGNITA.",
        "ActionGate sees medical, strong physics, social prediction, publication, external action or secret-like flags.",
        "Phi_eff stays at or below 0.60 after evidence compression and local validation.",
        "COMMS validator fails or WitnessLog hash-chain verification fails.",
    ]
    recommendations = [
        recommendation,
        "Use this engine as a local gate and handoff compiler, not as proof of physics or human diagnosis.",
        "For Claudio/Wabi-Sabi, consume the JSON result before writes and route REVIEW/BLOCK to human-visible handoff.",
    ]
    if inverse["hidden_bias_flags"]:
        recommendations.append("Reduce hidden observer bias before promotion: " + ", ".join(inverse["hidden_bias_flags"]))

    return {
        "schema": "medioevo.observacionista_engine_result.v1",
        "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "status": status,
        "source_hashes": source_hashes,
        "observationist_engineering": observation,
        "inverse_observationist_engineering": inverse,
        "action_gate": observation["gate"] if observation["gate"] == "BLOCK" else status.replace("PASS", "APPROVE"),
        "claim_state": claim_state,
        "falsifiers": falsifiers,
        "recommendations": recommendations,
    }


def print_json(data: object) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run SETO observacionista and inverse-observacionista gate.")
    parser.add_argument("--input", action="append", default=[], help="UTF-8 text/JSON/JSONL input path. May be repeated.")
    parser.add_argument("--text", help="Inline claim or action text to evaluate.")
    parser.add_argument("--out", help="Write JSON result to this path.")
    parser.add_argument("--json", action="store_true", help="Print JSON result.")
    args = parser.parse_args()

    paths = [Path(value).resolve() for value in args.input] or [DEFAULT_INBOX]
    result = build_result(paths, args.text)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.json or not args.out:
        print_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
