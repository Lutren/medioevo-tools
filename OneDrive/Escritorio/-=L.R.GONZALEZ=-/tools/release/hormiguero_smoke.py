from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APP_PATH = ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "apps" / "hormiguero_mission_control" / "app.py"
ENDPOINTS = [
    "/api/health",
    "/api/state",
    "/api/buildings",
    "/api/agents",
    "/api/city-registry",
]


def load_app():
    if not APP_PATH.exists():
        raise FileNotFoundError(APP_PATH)
    spec = importlib.util.spec_from_file_location("hormiguero_mission_control_app", APP_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not import {APP_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.app


def main() -> int:
    app = load_app()
    results: list[dict[str, object]] = []
    with app.test_client() as client:
        for endpoint in ENDPOINTS:
            response = client.get(endpoint)
            payload = response.get_json(silent=True)
            results.append(
                {
                    "endpoint": endpoint,
                    "status_code": response.status_code,
                    "json": isinstance(payload, dict),
                    "ok": 200 <= response.status_code < 300,
                }
            )
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0 if all(item["ok"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
