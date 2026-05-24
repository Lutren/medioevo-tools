from __future__ import annotations

import http.client
import importlib.util
import json
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path


SERVER_PATH = Path(__file__).resolve().parents[1] / "server.py"


def load_server_module():
    spec = importlib.util.spec_from_file_location("duat_lite_server", SERVER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_duat_lite_http_dashboard_and_api() -> None:
    module = load_server_module()
    server = ThreadingHTTPServer(("127.0.0.1", 0), module.make_handler())
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = server.server_address
        conn = http.client.HTTPConnection(host, port, timeout=5)
        conn.request("GET", "/")
        response = conn.getresponse()
        html = response.read().decode("utf-8")
        assert response.status == 200
        assert "DUAT Lite" in html
        assert "Operational State" in html

        conn.request("GET", "/api/health")
        response = conn.getresponse()
        health = json.loads(response.read().decode("utf-8"))
        assert response.status == 200
        assert health["status"] == "ok"
        assert health["publication_gate"] == "BLOCK"

        body = json.dumps({"text": "Causal Rendering prueba una nueva fisica."})
        conn.request("POST", "/api/classify", body=body, headers={"Content-Type": "application/json"})
        response = conn.getresponse()
        payload = json.loads(response.read().decode("utf-8"))
        assert response.status == 200
        assert payload["schemaVersion"] == "duat.lite.classify_response.v0_1"
        assert payload["result"]["gate"] == "BLOCK"
        assert payload["cloud_provider_called"] is False
        assert payload["applied_to_sources"] is False
    finally:
        server.shutdown()
        server.server_close()
