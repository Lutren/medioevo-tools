import time
import json
import threading
from typing import Dict, List, Optional

LOG_PATH = r"C:\Users\L-Tyr\claudio\logs\router_decisions.jsonl"

# Models configuration
MODELS = {
    "local": {
        "qwen2.5-coder:7b": {"type": "local"},
        "qwen3:8b": {"type": "local"},
        "qwen2.5-coder:3b": {"type": "local"},
        "qwen2.5:0.5b": {"type": "local"},
        "gemma4:latest": {"type": "local"},
    },
    "cloud": [
        "qwen3-coder:480b-cloud",
        "GLM-5.1:cloud",
        "nemotron-3-super:cloud",
        "qwen3.5:cloud",
    ],
}

# Task-type priority mapping -> list of preferred local models first
TASK_MAP = {
    "codigo": ["qwen2.5-coder:7b", "qwen2.5-coder:3b"],
    "refactor": ["qwen2.5-coder:7b", "qwen2.5-coder:3b"],
    "debug": ["qwen2.5-coder:7b", "qwen2.5-coder:3b"],
    "razonamiento": ["qwen3:8b"],
    "planning": ["qwen3:8b"],
    "trivial": ["qwen2.5:0.5b", "qwen2.5-coder:3b"],
}

# Timeouts and thresholds
LOCAL_TIMEOUT = 90.0  # seconds
CLOUD_TOKEN_THRESHOLD = 20000  # placeholder tokens threshold to force cloud

lock = threading.Lock()


def _log_decision(entry: Dict):
    entry["ts"] = int(time.time() * 1000)
    with lock:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


class Router:
    def __init__(self):
        self.cloud_order = MODELS["cloud"]

    def route(self, task_type: str, prompt_tokens: int, dry_run: bool = True, force_local_only: bool = False) -> Dict:
        start = time.time()
        task_type = task_type.lower()
        fallback_count = 0
        chosen = None
        reason = ""

        preferred_locals = TASK_MAP.get(task_type, ["qwen3:8b"])

        # If force local only, pick first available local in preferred list
        if force_local_only:
            for m in preferred_locals:
                if m in MODELS["local"]:
                    chosen = m
                    reason = "force_local_only"
                    break
            latency = int((time.time() - start) * 1000)
            _log_decision({"tarea": task_type, "modelo_elegido": chosen, "motivo": reason, "latencia_ms": latency, "fallback_count": fallback_count})
            return {"model": chosen, "reason": reason, "cascade": []}

        # If prompt tokens exceed threshold, go to cloud first
        if prompt_tokens >= CLOUD_TOKEN_THRESHOLD:
            # try cloud in order
            for cloud_model in self.cloud_order:
                chosen = cloud_model
                reason = "prompt_exceeds_threshold"
                latency = int((time.time() - start) * 1000)
                _log_decision({"tarea": task_type, "modelo_elegido": chosen, "motivo": reason, "latencia_ms": latency, "fallback_count": fallback_count})
                return {"model": chosen, "reason": reason, "cascade": self._build_cascade(preferred_locals)}

        # Try local preferred models first
        for m in preferred_locals:
            if m in MODELS["local"]:
                chosen = m
                reason = "local_preferred"
                # Simulate local call with timeout check placeholder (real call happens elsewhere)
                # If local "fails" (simulated by raising), we will escalate
                latency = int((time.time() - start) * 1000)
                _log_decision({"tarea": task_type, "modelo_elegido": chosen, "motivo": reason, "latencia_ms": latency, "fallback_count": fallback_count})
                return {"model": chosen, "reason": reason, "cascade": self._build_cascade(preferred_locals)}

        # If no local available, fallback to cloud sequence
        for cloud_model in self.cloud_order:
            chosen = cloud_model
            reason = "no_local_available"
            latency = int((time.time() - start) * 1000)
            _log_decision({"tarea": task_type, "modelo_elegido": chosen, "motivo": reason, "latencia_ms": latency, "fallback_count": fallback_count})
            return {"model": chosen, "reason": reason, "cascade": self._build_cascade(preferred_locals)}

        # Fallback final
        latency = int((time.time() - start) * 1000)
        _log_decision({"tarea": task_type, "modelo_elegido": chosen, "motivo": "unknown", "latencia_ms": latency, "fallback_count": fallback_count})
        return {"model": chosen, "reason": "unknown", "cascade": []}

    def _build_cascade(self, preferred_locals: List[str]) -> List[str]:
        cascade = []
        # local preferences
        for m in preferred_locals:
            if m in MODELS["local"]:
                cascade.append(m)
        # then cloud order
        cascade.extend(self.cloud_order)
        return cascade


if __name__ == "__main__":
    r = Router()
    print(r.route("codigo", 10))
