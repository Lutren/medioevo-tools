from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import sqlite3
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Protocol

from wabi_sabi.core.gate import ActionGate

try:  # Canonical OSIT regime / phi_eff come from obsai-core (single source of truth).
    from obsai_core import estimate_regime as _obsai_estimate_regime
    from obsai_core import phi_eff_power as _obsai_phi_eff_power
except Exception:  # pragma: no cover - dependency-light fallback if obsai-core is absent.
    _obsai_estimate_regime = None
    _obsai_phi_eff_power = None


# Mirrors obsai_core.metrics.estimate_regime. Canonical ladder documented in
# packages/open-dev/obsai-core/docs/OSIT_CANON_REUSE_CONTRACT_2026-05-29.md
_REGIME_BANDS = (
    (0.15, "OPTIMO"),
    (0.30, "FUNCIONAL"),
    (0.45, "PRE_JAMMING"),
    (0.60, "JAMMING_TEMPRANO"),
)
# Regimes where a low-residue conversation must never auto-APPROVE and the model is degraded.
JAMMING_REGIMES = {"JAMMING_TEMPRANO", "JAMMING"}
DEGRADED_MODEL_ID = "qwen2.5:0.5b"


def regime_for_residue(r_estimate: float) -> str:
    """Canonical OSIT regime label for a residue R in [0,1]."""
    if _obsai_estimate_regime is not None:
        return str(_obsai_estimate_regime(r_estimate).value)
    value = max(0.0, min(1.0, float(r_estimate)))
    for threshold, label in _REGIME_BANDS:
        if value < threshold:
            return label
    return "JAMMING"


def phi_eff_for_residue(r_estimate: float) -> float:
    """Canonical phi_eff for a residue R (obsai phi_eff_power; == 1-R under default params)."""
    if _obsai_phi_eff_power is not None:
        return round(float(_obsai_phi_eff_power(r_estimate)), 3)
    return round(max(0.0, 1.0 - max(0.0, min(1.0, float(r_estimate)))), 3)


DETERMINISTIC_WORDS = {
    "hash",
    "sha256",
    "listar",
    "list",
    "status",
    "estado",
    "conteo",
    "count",
    "validar json",
    "sqlite",
}

TRIAGE_WORDS = {
    "triage",
    "clasifica",
    "clasificar",
    "heartbeat",
    "resumen",
    "resume",
    "prioridad",
    "pendiente",
}

CODER_WORDS = {
    "arquitectura",
    "codigo",
    "code",
    "python",
    "test",
    "pytest",
    "refactor",
    "adapter",
    "modulo",
    "runtime",
}

BLOCK_WORDS = {
    "fine-tune",
    "finetune",
    "lora",
    "entrena pesos",
    "train weights",
    "alias ollama",
    "ollama create",
    "descarga modelo",
    "download model",
    "publica",
    "publish",
    "deploy",
    "push",
    "secret",
    "token",
    ".env",
}

UNCERTAIN_WORDS = {
    "quizas",
    "quiza",
    "maybe",
    "posiblemente",
    "creo",
    "hipotesis",
    "hipotesis",
    "incognito",
    "inferencia",
}


@dataclass
class TaskEnvelope:
    envelope_version: str = "wabi-osit-task-v1"
    created_at_utc: str = field(default_factory=lambda: dt.datetime.now(dt.UTC).isoformat())
    raw_text: str = ""
    intent: str = "general"
    evidence_refs: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)
    source: str = "local_cli"
    fingerprint: str = ""

    def finalize(self) -> "TaskEnvelope":
        payload = {
            "raw_text": self.raw_text,
            "intent": self.intent,
            "evidence_refs": self.evidence_refs,
            "risk_flags": self.risk_flags,
            "source": self.source,
        }
        self.fingerprint = hashlib.sha256(
            json.dumps(payload, sort_keys=True, ensure_ascii=True).encode("utf-8")
        ).hexdigest()
        return self


@dataclass(frozen=True)
class RouteDecision:
    gate: str
    route: str
    runtime: str
    model_id: str | None
    r_estimate: float
    phi_eff: float
    reasons: list[str]
    blocked_actions: list[str] = field(default_factory=list)
    required_evidence: list[str] = field(default_factory=list)
    regime: str = "FUNCIONAL"

    @property
    def allowed(self) -> bool:
        return self.gate == "APPROVE"


@dataclass(frozen=True)
class BridgeResult:
    envelope: TaskEnvelope
    decision: RouteDecision
    witness_event_id: int
    output: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "envelope": asdict(self.envelope),
            "decision": asdict(self.decision),
            "witness_event_id": self.witness_event_id,
            "output": self.output,
        }


class RuntimeAdapter(Protocol):
    name: str

    def execute(self, envelope: TaskEnvelope, decision: RouteDecision) -> dict[str, Any]:
        ...


class NoLLMAdapter:
    name = "deterministic_no_llm"

    def execute(self, envelope: TaskEnvelope, decision: RouteDecision) -> dict[str, Any]:
        return {
            "mode": self.name,
            "message": "Deterministic local plan only. No model runtime was called.",
            "next_actions": [
                "collect_evidence",
                "run_validator_or_test",
                "append_witness_event",
            ],
            "task_fingerprint": envelope.fingerprint,
        }


class MockRuntimeAdapter:
    def __init__(self, name: str = "mock_runtime") -> None:
        self.name = name
        self.calls: list[dict[str, Any]] = []

    def execute(self, envelope: TaskEnvelope, decision: RouteDecision) -> dict[str, Any]:
        payload = {"fingerprint": envelope.fingerprint, "model_id": decision.model_id}
        self.calls.append(payload)
        return {"mode": self.name, "message": "mock execution", "payload": payload}


class ResidueMeter:
    """Computable proxy for R until calibrated against real failures."""

    def estimate(self, envelope: TaskEnvelope) -> float:
        text = envelope.raw_text.lower()
        score = 0.10
        if not envelope.evidence_refs:
            score += 0.14
        if any(word in text for word in UNCERTAIN_WORDS):
            score += 0.12
        if any(word in text for word in CODER_WORDS):
            score += 0.08
        if any(word in text for word in BLOCK_WORDS):
            score += 0.35
        if any(flag in {"external", "secret", "destructive", "model_mutation"} for flag in envelope.risk_flags):
            score += 0.35
        if len(text) > 800:
            score += 0.08
        return max(0.0, min(1.0, round(score, 3)))


class BridgeActionGate:
    def evaluate(
        self, envelope: TaskEnvelope, r_estimate: float, regime: str = "FUNCIONAL"
    ) -> tuple[str, list[str], list[str]]:
        text = envelope.raw_text.lower()
        base_gate = ActionGate().evaluate_text(envelope.raw_text)
        reasons = list(base_gate.reasons)
        blocked_actions: list[str] = []

        if any(word in text for word in BLOCK_WORDS):
            reasons.append("blocked_boundary_word")
            blocked_actions.append("external_or_model_mutation")
        if any(flag in envelope.risk_flags for flag in ["secret", "destructive", "external", "model_mutation"]):
            reasons.append("risk_flag_requires_block")
            blocked_actions.extend(envelope.risk_flags)
        if base_gate.gate == "BLOCK" or blocked_actions:
            return "BLOCK", sorted(set(reasons)), sorted(set(blocked_actions))
        # Canonical OSIT regime never lets a jamming-band conversation auto-APPROVE.
        if regime in JAMMING_REGIMES:
            reasons.append(f"regime_{regime.lower()}_requires_review")
            return "REVIEW", sorted(set(reasons)), []
        if r_estimate >= 0.45:
            reasons.append("residue_requires_review")
            return "REVIEW", sorted(set(reasons)), []
        if any(word in text for word in ["modifica", "edita", "write", "crear archivo", "implementa"]):
            reasons.append("local_write_requires_scoped_review")
            return "REVIEW", sorted(set(reasons)), []
        return "APPROVE", sorted(set(reasons or ["low_residue_local_action"])), []


class ModelRegistry:
    def select(self, envelope: TaskEnvelope, gate: str) -> tuple[str, str, str | None, list[str]]:
        text = envelope.raw_text.lower()
        if gate == "BLOCK":
            return "blocked", "none", None, ["blocked_tasks_do_not_call_runtime"]
        if any(word in text for word in DETERMINISTIC_WORDS):
            return "deterministic", "deterministic_no_llm", None, ["deterministic_task_no_model"]
        if any(word in text for word in CODER_WORDS):
            return "technical_coder", "ollama_optional", "qwen2.5-coder:3b", ["technical_or_code_task"]
        if any(word in text for word in TRIAGE_WORDS):
            return "triage", "ollama_optional", "qwen2.5:0.5b", ["low_cost_triage_task"]
        return "triage", "ollama_optional", "qwen2.5:0.5b", ["default_small_model_for_low_risk_language"]


class WitnessLog:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS witness_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at_utc TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    previous_hash TEXT NOT NULL,
                    event_hash TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def append(self, event_type: str, payload: dict[str, Any]) -> int:
        created_at = dt.datetime.now(dt.UTC).isoformat()
        payload_json = json.dumps(payload, sort_keys=True, ensure_ascii=True)
        previous_hash = self.last_hash()
        event_hash = self.compute_hash(created_at, event_type, payload_json, previous_hash)
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO witness_events (
                    created_at_utc, event_type, payload_json, previous_hash, event_hash
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (created_at, event_type, payload_json, previous_hash, event_hash),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def last_hash(self) -> str:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT event_hash FROM witness_events ORDER BY id DESC LIMIT 1"
            ).fetchone()
        return str(row[0]) if row else "GENESIS"

    @staticmethod
    def compute_hash(created_at: str, event_type: str, payload_json: str, previous_hash: str) -> str:
        material = "|".join([previous_hash, created_at, event_type, payload_json])
        return hashlib.sha256(material.encode("utf-8")).hexdigest()

    def verify_chain(self) -> tuple[bool, str]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, created_at_utc, event_type, payload_json, previous_hash, event_hash
                FROM witness_events
                ORDER BY id ASC
                """
            ).fetchall()
        expected_previous = "GENESIS"
        for row in rows:
            row_id, created_at, event_type, payload_json, previous_hash, event_hash = row
            if previous_hash != expected_previous:
                return False, f"previous_hash_mismatch_at:{row_id}"
            expected_hash = self.compute_hash(created_at, event_type, payload_json, previous_hash)
            if event_hash != expected_hash:
                return False, f"event_hash_mismatch_at:{row_id}"
            expected_previous = event_hash
        return True, "ok"


class BridgeExecutor:
    def __init__(
        self,
        witness_db: str | Path,
        *,
        runtime_adapter: RuntimeAdapter | None = None,
        residue_meter: ResidueMeter | None = None,
    ) -> None:
        self.witness = WitnessLog(witness_db)
        self.runtime_adapter = runtime_adapter or NoLLMAdapter()
        self.residue_meter = residue_meter or ResidueMeter()
        self.gate = BridgeActionGate()
        self.registry = ModelRegistry()

    def execute(
        self,
        raw_text: str,
        *,
        intent: str = "general",
        evidence_refs: list[str] | None = None,
        source: str = "local_cli",
    ) -> BridgeResult:
        envelope = TaskEnvelope(
            raw_text=raw_text,
            intent=intent,
            evidence_refs=list(evidence_refs or []),
            risk_flags=self._risk_flags(raw_text),
            source=source,
        ).finalize()
        r_estimate = self.residue_meter.estimate(envelope)
        regime = regime_for_residue(r_estimate)
        gate, gate_reasons, blocked_actions = self.gate.evaluate(envelope, r_estimate, regime)
        route, runtime, model_id, route_reasons = self.registry.select(envelope, gate)
        # Degrade to the smallest model when the residue regime is in the jamming band.
        if regime in JAMMING_REGIMES and model_id and model_id != DEGRADED_MODEL_ID:
            model_id = DEGRADED_MODEL_ID
            route_reasons = [*route_reasons, f"regime_{regime.lower()}_degrade_to_small_model"]
        decision = RouteDecision(
            gate=gate,
            route=route,
            runtime=runtime,
            model_id=model_id,
            r_estimate=r_estimate,
            phi_eff=phi_eff_for_residue(r_estimate),
            reasons=sorted(set(gate_reasons + route_reasons)),
            blocked_actions=blocked_actions,
            required_evidence=[] if evidence_refs else ["source_hash_or_test_or_local_file_reference"],
            regime=regime,
        )
        if gate == "BLOCK":
            output = {
                "mode": "blocked",
                "message": "ActionGate blocked runtime execution.",
                "next_actions": ["add_evidence", "reduce_scope", "request_human_gate_if_needed"],
            }
        else:
            output = self.runtime_adapter.execute(envelope, decision)
        event_id = self.witness.append(
            "bridge_decision",
            {
                "envelope": asdict(envelope),
                "decision": asdict(decision),
                "output": output,
            },
        )
        return BridgeResult(envelope=envelope, decision=decision, witness_event_id=event_id, output=output)

    @staticmethod
    def _risk_flags(text: str) -> list[str]:
        lowered = text.lower()
        flags: set[str] = set()
        if any(word in lowered for word in ["delete", "borrar", "remove", "rm -rf", "format"]):
            flags.add("destructive")
        if any(word in lowered for word in ["push", "deploy", "publica", "linkedin", "gumroad"]):
            flags.add("external")
        if any(word in lowered for word in ["secret", "token", ".env", "credential", "api key"]):
            flags.add("secret")
        if any(word in lowered for word in ["fine-tune", "finetune", "lora", "alias ollama", "ollama create"]):
            flags.add("model_mutation")
        if re.search(r"\b(diagnostico medico|prediccion social|garantiza seguridad|nueva fisica probada)\b", lowered):
            flags.add("strong_claim")
        return sorted(flags)
