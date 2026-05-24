from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OBSAI_CORE = ROOT / "packages" / "open-dev" / "obsai-core"
INDEX_HTML = Path(__file__).with_name("index.html")
if str(OBSAI_CORE) not in sys.path:
    sys.path.insert(0, str(OBSAI_CORE))

from obsai_core.epistemic_engine import OSITEpistemicEngine  # noqa: E402


def make_handler(engine: OSITEpistemicEngine | None = None) -> type[BaseHTTPRequestHandler]:
    api_engine = engine or OSITEpistemicEngine()

    class DUATLiteHandler(BaseHTTPRequestHandler):
        server_version = "duat-lite/0.1"

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            return

        def do_GET(self) -> None:  # noqa: N802
            if self.path in {"/", "/index.html"}:
                _write_bytes(self, 200, INDEX_HTML.read_bytes(), "text/html; charset=utf-8")
                return
            if self.path == "/api/health":
                _write_json(self, 200, {
                    "schemaVersion": "duat.lite.health.v0_1",
                    "status": "ok",
                    "engine": api_engine.health(),
                    "publication_gate": "BLOCK",
                    "cloud_provider_called": False,
                })
                return
            _write_json(self, 404, {"error": "not_found"})

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/api/classify":
                _write_json(self, 404, {"error": "not_found"})
                return
            try:
                payload = _read_json_body(self)
                text = str(payload.get("text", payload.get("input", "")))
                task = str(payload.get("task", "duat_lite_review"))
                result = api_engine.classify_text(text, task=task)
            except ValueError as exc:
                _write_json(self, 400, {"error": str(exc)})
                return
            except json.JSONDecodeError:
                _write_json(self, 400, {"error": "invalid_json"})
                return
            _write_json(self, 200, {
                "schemaVersion": "duat.lite.classify_response.v0_1",
                "status": "OK",
                "result": result,
                "publication_gate": "BLOCK",
                "cloud_provider_called": False,
                "applied_to_sources": False,
            })

    return DUATLiteHandler


def run_server(host: str = "127.0.0.1", port: int = 8790) -> None:
    server = ThreadingHTTPServer((host, port), make_handler())
    try:
        print(f"DUAT Lite listening on http://{host}:{port}", flush=True)
        server.serve_forever()
    finally:
        server.server_close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="DUAT Lite local dashboard.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8790)
    args = parser.parse_args(argv)
    run_server(host=args.host, port=args.port)
    return 0


def _read_json_body(handler: BaseHTTPRequestHandler) -> dict[str, Any]:
    length = int(handler.headers.get("content-length", "0"))
    raw = handler.rfile.read(length).decode("utf-8")
    data = json.loads(raw or "{}")
    if not isinstance(data, dict):
        raise ValueError("json_object_required")
    return data


def _write_json(handler: BaseHTTPRequestHandler, status: int, payload: dict[str, Any]) -> None:
    body = json.dumps(payload, ensure_ascii=True, sort_keys=True).encode("utf-8")
    _write_bytes(handler, status, body, "application/json; charset=utf-8")


def _write_bytes(handler: BaseHTTPRequestHandler, status: int, body: bytes, content_type: str) -> None:
    handler.send_response(status)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


if __name__ == "__main__":
    raise SystemExit(main())
