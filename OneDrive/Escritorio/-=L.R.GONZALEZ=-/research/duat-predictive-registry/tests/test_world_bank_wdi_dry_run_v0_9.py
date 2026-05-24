from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from data_readiness.world_bank_wdi_dry_run_v0_9 import RUN_ID, run_wdi_backtest_dry_run


ROOT = Path(__file__).resolve().parents[1]


def test_wdi_dry_run_keeps_review_and_publication_block():
    report = run_wdi_backtest_dry_run(ROOT)
    assert report["run_id"] == RUN_ID
    assert report["DataGate"] == "REVIEW"
    assert report["BacktestOpenGate"] == "REVIEW_ONLY_DRY_RUN"
    assert report["publication_gate"] == "BLOCK"
    assert report["status"] == "REVIEW_INTERNAL_ONLY"
    assert report["benchmark_public"] is False
    assert report["model_claim_allowed"] is False
    assert report["ranking_allowed"] is False
    assert report["causal_claim_allowed"] is False


def test_wdi_dry_run_has_no_leakage_or_recalibration():
    report = run_wdi_backtest_dry_run(ROOT)
    assert report["leakage_preflight"]["status"] == "PASS"
    assert report["summary"]["series_count"] == 3
    assert report["summary"]["total_dry_run_folds"] > 0
    for item in report["series"]:
        policy = item["dry_run_policy"]
        assert policy["uses_future_data"] is False
        assert policy["tunes_model"] is False
        assert policy["uses_holdout_for_recalibration"] is False
        assert policy["public_claim_allowed"] is False


def test_wdi_dry_run_script_writes_report():
    result = subprocess.run(
        [sys.executable, "scripts/run_wdi_backtest_dry_run_v0_9.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["run_id"] == RUN_ID
    assert payload["publication_gate"] == "BLOCK"
    assert (ROOT / "reports" / "duat-world-bank-wdi-backtest-dry-run-v0-9.json").exists()
    assert (ROOT / "reports" / "DUAT_WORLD_BANK_WDI_BACKTEST_DRY_RUN_v0_9.md").exists()
