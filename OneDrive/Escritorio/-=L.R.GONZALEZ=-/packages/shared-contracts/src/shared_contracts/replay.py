from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def replay_hash(*, seed: str, payload: Any, prev_hash: str = "GENESIS") -> str:
    envelope = {
        "schema_version": "medioevo.replay_hash.v0.1",
        "seed": seed,
        "prev_hash": prev_hash,
        "payload": payload,
    }
    return hashlib.sha256(canonical_json(envelope).encode("utf-8")).hexdigest()

