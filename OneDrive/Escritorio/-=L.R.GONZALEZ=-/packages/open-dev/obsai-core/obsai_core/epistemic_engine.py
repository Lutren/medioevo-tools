"""Dependency-free OSIT epistemic engine API.

The engine wraps ClaimClassifier and ObservationEnvelope v2.1 behind a small
local API surface. It is local-only by default and carries explicit publication
and calibration gates.
"""

from __future__ import annotations

import hashlib
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .claim_classifier import ClaimClassifier

ENGINE_SCHEMA = "obsai.osit_epistemic_engine.response.v1"
HEALTH_SCHEMA = "obsai.osit_epistemic_engine.health.v1"
PIPELINE_STEPS = (
    "INTAKE",
    "TRUTHGATE",
    "DO",
    "C-GATE",
    "ScienceClaimGate",
    "IOI",
    "TEST",
    "SOURCECARD",
)


class OSITEpistemicEngine:
    """Minimal local OSIT/MOI engine."""

    def __init__(self, classifier: ClaimClassifier | None = None) -> None:
        self.classifier = classifier or ClaimClassifier(agent_name="OSITEpistemicEngine")

    def health(self) -> dict[str, Any]:
        return {
            "schemaVersion": HEALTH_SCHEMA,
            "status": "ok",
            "engine": "OSITEpistemicEngine",
            "endpoints": ["/health", "/classify"],
            "pipeline": list(PIPELINE_STEPS),
            "calibration": "DEMO_ONLY",
            "publication_gate": "BLOCK",
            "cloud_provider_called": False,
        }

    def classify_text(self, text: str, task: str = "osit_epistemic_engine") -> dict[str, Any]:
        clean_text = str(text or "").strip()
        if not clean_text:
            raise ValueError("text_required")
        clean_task = str(task or "osit_epistemic_engine").strip() or "osit_epistemic_engine"
        envelope = self.classifier.classify(clean_text, task=clean_task)
        envelope_payload = envelope.to_dict()
        source_card = _source_card(clean_text, clean_task, envelope_payload)
        return {
            "schemaVersion": ENGINE_SCHEMA,
            "status": "OK",
            "engine": "OSITEpistemicEngine",
            "task": clean_task,
            "pipeline": list(PIPELINE_STEPS),
            "observation_envelope": envelope_payload,
            "source_card": source_card,
            "claim_count": len(envelope_payload.get("claims", [])),
            "gate": envelope_payload.get("gate", "REVIEW"),
            "R_or": envelope_payload.get("R_or"),
            "phi_moi": envelope_payload.get("phi_moi"),
            "next_action": envelope_payload.get("next_action", ""),
            "calibration": "DEMO_ONLY",
            "publication_gate": "BLOCK",
            "cloud_provider_called": False,
            "applied_to_sources": False,
        }


def classify_text(text: str, task: str = "osit_epistemic_engine") -> dict[str, Any]:
    return OSITEpistemicEngine().classify_text(text, task=task)


def make_epistemic_handler(engine: OSITEpistemicEngine | None = None) -> type[BaseHTTPRequestHandler]:
    api_engine = engine or OSITEpistemicEngine()

    class EpistemicHandler(BaseHTTPRequestHandler):
        server_version = "obsai-epistemic-engine/0.1"

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            return

        def do_GET(self) -> None:  # noqa: N802
            if self.path in {"/", "/health"}:
                _write_json(self, 200, api_engine.health())
                return
            _write_json(self, 404, {"error": "not_found", "endpoints": ["/health", "/classify"]})

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/classify":
                _write_json(self, 404, {"error": "not_found", "endpoints": ["/health", "/classify"]})
                return
            try:
                payload = _read_json_body(self)
                text = payload.get("text", payload.get("input", ""))
                task = str(payload.get("task", "osit_epistemic_engine"))
                output = api_engine.classify_text(str(text), task=task)
            except ValueError as exc:
                _write_json(self, 400, {"error": str(exc)})
                return
            except json.JSONDecodeError:
                _write_json(self, 400, {"error": "invalid_json"})
                return
            _write_json(self, 200, output)

    return EpistemicHandler


def run_epistemic_server(host: str = "127.0.0.1", port: int = 8789) -> None:
    server = ThreadingHTTPServer((host, port), make_epistemic_handler())
    try:
        server.serve_forever()
    finally:
        server.server_close()


def _read_json_body(handler: BaseHTTPRequestHandler) -> dict[str, Any]:
    length = int(handler.headers.get("content-length", "0"))
    raw = handler.rfile.read(length).decode("utf-8")
    data = json.loads(raw or "{}")
    if not isinstance(data, dict):
        raise ValueError("json_object_required")
    return data


def _write_json(handler: BaseHTTPRequestHandler, status: int, payload: dict[str, Any]) -> None:
    body = json.dumps(payload, ensure_ascii=True, sort_keys=True).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _source_card(text: str, task: str, envelope: dict[str, Any]) -> dict[str, Any]:
    digest = hashlib.sha256(f"{task}\n{text}".encode("utf-8")).hexdigest()
    return {
        "schemaVersion": "obsai.source_card.v1",
        "id": f"source-card-{digest[:16]}",
        "sha256": digest,
        "source_type": "local_text",
        "task": task,
        "claim_count": len(envelope.get("claims", [])),
        "gate": envelope.get("gate", "REVIEW"),
        "R_or": envelope.get("R_or"),
        "phi_moi": envelope.get("phi_moi"),
        "falsifier": envelope.get("falsifier"),
        "next_action": envelope.get("next_action", ""),
        "publication_gate": "BLOCK",
    }
