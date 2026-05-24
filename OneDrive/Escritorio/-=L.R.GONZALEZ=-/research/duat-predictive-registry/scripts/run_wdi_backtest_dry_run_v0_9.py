from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from data_readiness.world_bank_wdi_dry_run_v0_9 import run_wdi_backtest_dry_run, write_dry_run_report


def main() -> int:
    report = run_wdi_backtest_dry_run(ROOT)
    payload_sha, file_sha = write_dry_run_report(
        report,
        ROOT / "reports" / "duat-world-bank-wdi-backtest-dry-run-v0-9.json",
        ROOT / "reports" / "DUAT_WORLD_BANK_WDI_BACKTEST_DRY_RUN_v0_9.md",
    )
    print(
        json.dumps(
            {
                "run_id": report["run_id"],
                "status": report["status"],
                "DataGate": report["DataGate"],
                "BacktestGate": report["BacktestOpenGate"],
                "publication_gate": report["publication_gate"],
                "payload_sha256": payload_sha,
                "file_sha256": file_sha,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["status"] != "BLOCK" else 2


if __name__ == "__main__":
    raise SystemExit(main())
