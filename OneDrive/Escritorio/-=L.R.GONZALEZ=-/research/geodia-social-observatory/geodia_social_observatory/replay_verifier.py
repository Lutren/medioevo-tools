"""Replay verification for DUAT Smallville v0.2."""

from __future__ import annotations

from typing import Any

from .contracts import DUAT_SMALLVILLE_REPLAY_SCHEMA
from .intervention_engine import run_smallville_v0_2
from .smallville_lab import stable_hash


def verify_v0_2_hash_chain(ledger: dict[str, Any]) -> bool:
    previous_hash = "GENESIS"
    for event in ledger.get("events", []):
        observed_hash = event.get("event_hash")
        body = {key: value for key, value in event.items() if key != "event_hash"}
        if body.get("previous_hash") != previous_hash:
            return False
        if stable_hash(body) != observed_hash:
            return False
        previous_hash = observed_hash
    return previous_hash == ledger.get("fingerprints", {}).get("last_event_hash")


def verify_replay(ledger: dict[str, Any], pack: dict[str, Any]) -> dict[str, Any]:
    replayed = run_smallville_v0_2(seed=int(ledger["seed"]), ticks=int(ledger["ticks"]), pack=pack, intervention_name=ledger.get("intervention"))
    expected = ledger.get("fingerprints", {}).get("ledger_sha256")
    observed = replayed.get("fingerprints", {}).get("ledger_sha256")
    hash_chain_valid = verify_v0_2_hash_chain(ledger)
    passed = expected == observed and hash_chain_valid
    return {
        "schema": DUAT_SMALLVILLE_REPLAY_SCHEMA,
        "run_id": "DUAT_SMALLVILLE_REPLAY_VERIFICATION_v0_2",
        "seed": ledger["seed"],
        "ticks": ledger["ticks"],
        "expected_hash": expected,
        "observed_hash": observed,
        "hash_chain_valid": hash_chain_valid,
        "replay_verified": passed,
        "status": "REPLAY_PASS" if passed else "REPLAY_FAIL",
        "boundary": {
            "uses_real_data": False,
            "uses_network": False,
            "uses_credentials": False,
            "publication_gate": "BLOCK",
        },
    }


__all__ = ["verify_replay", "verify_v0_2_hash_chain"]
