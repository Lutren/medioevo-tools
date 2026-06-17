from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
QUEUE_PATH = ROOT / "runtime" / "production_autopilot" / "elevenlabs_voice_queue.jsonl"
REPORT_PATH = ROOT / "runtime" / "production_autopilot" / "elevenlabs_voice_bridge_report.json"


def load_queue(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    items: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            items.append(payload)
    return items


def res_to_path(res_path: str) -> Path:
    if not res_path.startswith("res://"):
        raise ValueError(f"Expected res:// path, got {res_path}")
    return ROOT / res_path.replace("res://", "").replace("/", "\\")


def synthesize(api_key: str, item: dict[str, Any], model_id: str) -> dict[str, Any]:
    voice_id = str(item.get("elevenlabs_voice_id", ""))
    if voice_id in ["", "pending"]:
        return {"ok": False, "skipped": True, "reason": "voice_id_pending", "id": item.get("id", "")}
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    body = json.dumps(
        {
            "text": str(item.get("text", "")),
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.48,
                "similarity_boost": 0.72,
                "style": 0.18,
                "use_speaker_boost": True,
            },
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            audio = response.read()
    except urllib.error.HTTPError as exc:
        return {"ok": False, "id": item.get("id", ""), "status": exc.code, "error": exc.read().decode("utf-8", errors="replace")[:800]}

    output_path = res_to_path(str(item.get("output_res_path", ""))).with_suffix(".mp3")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(audio)
    return {"ok": True, "id": item.get("id", ""), "output_path": str(output_path), "bytes": len(audio)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Safe ElevenLabs queue bridge for MEDIOEVO.")
    parser.add_argument("--queue", default=str(QUEUE_PATH))
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--model-id", default="eleven_multilingual_v2")
    parser.add_argument("--execute", action="store_true", help="Actually call ElevenLabs. Default is dry-run.")
    args = parser.parse_args()

    items = load_queue(Path(args.queue))[: max(0, args.limit)]
    api_key_present = bool(os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVEN_LABS_API_KEY"))
    report: dict[str, Any] = {
        "schema": "medioevo.ElevenLabsBridgeReport.v1",
        "queue": str(args.queue),
        "items_seen": len(items),
        "execute": args.execute,
        "api_key_present": api_key_present,
        "api_key_value_written": False,
        "results": [],
    }
    if not args.execute:
        report["results"] = [{"ok": True, "dry_run": True, "id": item.get("id", ""), "speaker": item.get("speaker", "")} for item in items]
    else:
        api_key = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVEN_LABS_API_KEY")
        if not api_key:
            report["results"].append({"ok": False, "reason": "missing_api_key_env"})
        else:
            for item in items:
                report["results"].append(synthesize(api_key, item, args.model_id))

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if all(bool(item.get("ok", False)) for item in report["results"]) else 2


if __name__ == "__main__":
    raise SystemExit(main())
