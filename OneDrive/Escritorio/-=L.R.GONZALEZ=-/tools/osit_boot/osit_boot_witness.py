#!/usr/bin/env python3
"""OSIT boot witness — Windows logon governance using obsai-core.

At logon this samples a few cheap OS health signals, computes the canonical OSIT
residue R and regime (``obsai_core.estimate_residue_from_signals`` /
``estimate_regime``), runs the canonical action gate (``obsai_core.evaluate_action``)
and appends a tamper-evident JSONL witness entry (chained by ``stable_fingerprint``).

It is **read-only** with respect to the system: it never changes settings, never
touches the BIOS/UEFI, and only writes its own log. Calibration is DEMO_ONLY.
Registration is a plain per-user logon task (see ``register_osit_boot_task.ps1``)
and is fully reversible.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


def _load_obsai():
    """Import the canonical obsai-core symbols, falling back to the editable repo path."""
    try:
        from obsai_core import (
            estimate_regime,
            estimate_residue_from_signals,
            evaluate_action,
            stable_fingerprint,
        )

        return estimate_regime, estimate_residue_from_signals, evaluate_action, stable_fingerprint
    except Exception:
        here = Path(__file__).resolve()
        for parent in here.parents:
            candidate = parent / "packages" / "open-dev" / "obsai-core"
            if (candidate / "obsai_core" / "__init__.py").exists():
                sys.path.insert(0, str(candidate))
                from obsai_core import (
                    estimate_regime,
                    estimate_residue_from_signals,
                    evaluate_action,
                    stable_fingerprint,
                )

                return estimate_regime, estimate_residue_from_signals, evaluate_action, stable_fingerprint
        raise


def sample_signals() -> list[str]:
    """Cheap stdlib OS health signals mapped to obsai ``JAMMING_SIGNALS``. DEMO_ONLY proxy."""
    signals: list[str] = []
    drive = (os.environ.get("SystemDrive", "C:") + os.sep) if os.name == "nt" else "/"
    try:
        total, _used, free = shutil.disk_usage(drive)
        free_ratio = (free / total) if total else 1.0
        if free_ratio < 0.10:
            signals.append("overload")  # < 10% free disk -> system pressure
        elif free_ratio < 0.20:
            signals.append("latency")  # < 20% free disk
    except Exception:
        signals.append("unresolved_tasks")  # could not read disk state
    try:
        tmp = Path(os.environ.get("TEMP") or os.environ.get("TMP") or "/tmp")
        if tmp.exists() and sum(1 for _ in tmp.iterdir()) > 2000:
            signals.append("unresolved_tasks")  # temp bloat
    except Exception:
        pass
    return signals


def build_witness_entry(signals, *, regime, residue, evaluate_action, stable_fingerprint, previous_hash):
    """Build one witness entry: OS residue/regime + the canonical action-gate verdict."""
    action = {
        "action_type": "system_boot_check",
        "input": "OSIT boot witness logon sample",
        "output": f"signals={signals} R={residue} regime={regime}",
        "risk": min(0.95, float(residue)),
        "reversibility": 1.0,  # read-only sample; no system change
        "sources": [{"verified": True, "confidence": 0.9, "id": "local_os_sample"}],
        "self_check": {"summary": "logon OS health sample", "uncertainties": list(signals)},
    }
    gate_result = evaluate_action(action)
    body = {
        "schema": "osit.boot_witness.v1",
        "timestampUtc": datetime.now(timezone.utc).isoformat(),
        "host": platform.node(),
        "platform": platform.platform(),
        "signals": list(signals),
        "R": residue,
        "regime": regime,
        "gate": gate_result["status"],
        "theta": gate_result["theta"],
        "previousHash": previous_hash,
        "calibration": "DEMO_ONLY",
    }
    body["fingerprint"] = stable_fingerprint({k: v for k, v in body.items() if k != "fingerprint"})
    return body


def last_hash(log_path: Path) -> str:
    """Fingerprint of the last witness entry (for chaining), or GENESIS."""
    if not log_path.exists():
        return "GENESIS"
    last = "GENESIS"
    try:
        with log_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    last = json.loads(line).get("fingerprint", last)
                except json.JSONDecodeError:
                    continue
    except Exception:
        return "GENESIS"
    return last


def default_log_path() -> Path:
    return Path.home() / ".medioevo" / "osit_boot" / "osit_boot_witness.jsonl"


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):  # es-MX accents survive a cp1252 console.
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    parser = argparse.ArgumentParser(description="OSIT boot witness (obsai-core canonical gate)")
    parser.add_argument("--log", default=str(default_log_path()), help="witness log path (JSONL)")
    parser.add_argument("--dry-run", action="store_true", help="print the entry but do not append to the log")
    parser.add_argument("--signal", action="append", default=[], help="inject an extra OSIT signal (repeatable)")
    args = parser.parse_args(argv)

    estimate_regime, estimate_residue_from_signals, evaluate_action, stable_fingerprint = _load_obsai()
    signals = sample_signals() + list(args.signal)
    residue = round(float(estimate_residue_from_signals(signals)), 6)
    regime = estimate_regime(residue).value

    log_path = Path(args.log)
    previous = "DRY_RUN" if args.dry_run else last_hash(log_path)
    entry = build_witness_entry(
        signals,
        regime=regime,
        residue=residue,
        evaluate_action=evaluate_action,
        stable_fingerprint=stable_fingerprint,
        previous_hash=previous,
    )
    line = json.dumps(entry, ensure_ascii=False)

    if args.dry_run:
        print("DRY-RUN (no se escribió el log):")
        print(line)
    else:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(line + "\n")
        print(f"OSIT boot witness -> {log_path}")
        print(f"  regime={regime} R={residue} gate={entry['gate']} fp={entry['fingerprint'][:12]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
