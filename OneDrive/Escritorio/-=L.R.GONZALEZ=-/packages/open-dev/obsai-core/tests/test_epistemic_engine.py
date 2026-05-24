from __future__ import annotations

import http.client
import json
import subprocess
import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

from obsai_core.epistemic_engine import ENGINE_SCHEMA, OSITEpistemicEngine, make_epistemic_handler


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_epistemic_engine_returns_observation_envelope_and_source_card() -> None:
    payload = OSITEpistemicEngine().classify_text("2 + 2 = 4", task="unit-test")

    assert payload["schemaVersion"] == ENGINE_SCHEMA
    assert payload["status"] == "OK"
    assert payload["publication_gate"] == "BLOCK"
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False
    assert payload["observation_envelope"]["schemaVersion"] == "obsai.observation_envelope.v2.1"
    assert payload["source_card"]["schemaVersion"] == "obsai.source_card.v1"
    assert payload["claim_count"] >= 1
    assert payload["observation_envelope"]["claims"][0]["gate_contract"]["schemaVersion"] == "obsai.claim_gate_contract.v1"


def test_epistemic_engine_blocks_strong_science_claim() -> None:
    payload = OSITEpistemicEngine().classify_text("Causal Rendering prueba una nueva fisica.")

    assert payload["gate"] == "BLOCK"
    claim = payload["observation_envelope"]["claims"][0]
    assert claim["label"] == "BLOQUEO"
    assert claim["gate_contract"]["final_decision"] == "BLOCK"


def test_epistemic_http_health_and_classify() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_epistemic_handler(OSITEpistemicEngine()))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = server.server_address
        conn = http.client.HTTPConnection(host, port, timeout=5)
        conn.request("GET", "/health")
        response = conn.getresponse()
        health = json.loads(response.read().decode("utf-8"))
        assert response.status == 200
        assert health["status"] == "ok"

        body = json.dumps({"text": "El observador no observa desde cero; observa desde estado."})
        conn.request("POST", "/classify", body=body, headers={"Content-Type": "application/json"})
        response = conn.getresponse()
        payload = json.loads(response.read().decode("utf-8"))
        assert response.status == 200
        assert payload["schemaVersion"] == ENGINE_SCHEMA
        assert payload["gate"] == "APPROVE"
    finally:
        server.shutdown()
        server.server_close()


def test_cli_classify_text_outputs_json() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "obsai_core.cli",
            "classify-text",
            "--text",
            "2 + 2 = 4",
        ],
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        timeout=30,
    )

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["schemaVersion"] == ENGINE_SCHEMA
    assert payload["publication_gate"] == "BLOCK"
