from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from geodia_social_observatory.cli import main as cli_main
from geodia_social_observatory.intervention_engine import build_baseline_intervention_pair
from geodia_social_observatory.metrics_v0_2 import build_metrics_v0_2, falsify_v0_2
from geodia_social_observatory.replay_verifier import verify_replay
from geodia_social_observatory.signal_source_pack import assert_no_real_data_or_credentials, build_signal_source_pack
from geodia_social_observatory.synthetic_environment_channels import (
    build_channel_observations,
    fuse_environment_channels,
)


class SmallvilleDuatV02Tests(unittest.TestCase):
    def test_signal_source_pack_schema_valid(self) -> None:
        pack = build_signal_source_pack(seed=20260517, ticks=12)
        self.assertEqual(pack["schema"], "duat.smallville.signal_source_pack.v0_2")
        self.assertEqual(pack["pack_id"], "duat_signal_source_pack_v0_2")
        self.assertEqual(pack["time_model"]["tick_seconds"], 10)
        self.assertEqual(pack["time_model"]["ticks"], 12)
        self.assertEqual(set(pack["channels"]), {"weather", "geophysics", "social_pressure", "infrastructure", "resource_availability"})
        self.assertEqual(pack["boundary"]["publication_gate"], "BLOCK")

    def test_signal_source_pack_deterministic_seed(self) -> None:
        first = build_signal_source_pack(seed=20260517, ticks=12)
        second = build_signal_source_pack(seed=20260517, ticks=12)
        other = build_signal_source_pack(seed=20260518, ticks=12)
        self.assertEqual(first["fingerprint"], second["fingerprint"])
        self.assertNotEqual(first["fingerprint"], other["fingerprint"])

    def test_no_real_data_or_credentials(self) -> None:
        pack = build_signal_source_pack(seed=20260517, ticks=12)
        result = assert_no_real_data_or_credentials(pack)
        self.assertTrue(result["passed"])
        self.assertFalse(result["values_printed"])

    def test_environment_channels_have_calibration_latency_noise(self) -> None:
        pack = build_signal_source_pack(seed=20260517, ticks=12)
        observations = build_channel_observations(pack, 0)
        for channel in observations.values():
            self.assertIn("latency", channel)
            self.assertIn("bandwidth", channel)
            self.assertIn("calibration", channel)
            self.assertIn("noise", channel)
            self.assertIn("missingness", channel)
            self.assertIn("contradiction", channel)

    def test_mts_fusion_preserves_contradiction(self) -> None:
        observations = {
            name: {
                "phi_eff_i": 0.92,
                "bandwidth": 0.9,
                "calibration": 0.9,
                "r_total": 0.1,
                "missingness": 0.0,
                "contradiction": 0.0,
            }
            for name in ("weather", "geophysics", "social_pressure", "infrastructure", "resource_availability")
        }
        observations["social_pressure"]["contradiction"] = 0.62
        fused = fuse_environment_channels(observations)
        self.assertEqual(fused["gate"], "REVIEW")
        self.assertGreaterEqual(fused["R_contradiction"], 0.5)

    def test_intervention_changes_metrics(self) -> None:
        pair = build_baseline_intervention_pair(seed=20260517, ticks=12)
        delta = pair["delta"]["intervention_delta"]
        self.assertGreater(delta["changed_agent_count"], 0)
        self.assertNotEqual(delta["delta_R_mean"], 0)
        self.assertNotEqual(delta["delta_Phi_eff_mean"], 0)

    def test_replay_same_seed_same_hash(self) -> None:
        pair = build_baseline_intervention_pair(seed=20260517, ticks=12)
        replay = verify_replay(pair["baseline"], pair["pack"])
        self.assertTrue(replay["replay_verified"])
        self.assertEqual(replay["status"], "REPLAY_PASS")

    def test_jamming_gate_triggers_at_threshold(self) -> None:
        observations = {
            name: {
                "phi_eff_i": 0.35,
                "bandwidth": 0.7,
                "calibration": 0.75,
                "r_total": 0.62,
                "missingness": 0.1,
                "contradiction": 0.0,
            }
            for name in ("weather", "geophysics", "social_pressure", "infrastructure", "resource_availability")
        }
        fused = fuse_environment_channels(observations)
        self.assertGreaterEqual(fused["fusion_R"], 0.45)
        self.assertIn(fused["gate"], {"REVIEW", "BLOCK"})
        self.assertIn(fused["regime"], {"PRE_JAMMING", "JAMMING"})

    def test_cli_smallville_signal_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pack.json"
            rc = cli_main(["smallville-signal-pack", "--ticks", "12", "--pretty", "--out", str(out)])
            pack = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(rc, 0)
        self.assertEqual(pack["schema"], "duat.smallville.signal_source_pack.v0_2")

    def test_cli_smallville_intervene(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            baseline = Path(tmp) / "baseline.json"
            intervention = Path(tmp) / "intervention.json"
            delta = Path(tmp) / "delta.json"
            rc = cli_main(
                [
                    "smallville-intervene",
                    "--ticks",
                    "12",
                    "--baseline-out",
                    str(baseline),
                    "--intervention-out",
                    str(intervention),
                    "--delta-out",
                    str(delta),
                    "--pretty",
                ]
            )
            delta_payload = json.loads(delta.read_text(encoding="utf-8"))
        self.assertEqual(rc, 0)
        self.assertTrue(delta_payload["hash_linked"])
        self.assertGreater(delta_payload["intervention_delta"]["changed_agent_count"], 0)

    def test_cli_smallville_replay_verify(self) -> None:
        pair = build_baseline_intervention_pair(seed=20260517, ticks=12)
        with tempfile.TemporaryDirectory() as tmp:
            pack_path = Path(tmp) / "pack.json"
            ledger_path = Path(tmp) / "ledger.json"
            replay_path = Path(tmp) / "replay.json"
            pack_path.write_text(json.dumps(pair["pack"]), encoding="utf-8")
            ledger_path.write_text(json.dumps(pair["baseline"]), encoding="utf-8")
            rc = cli_main(["smallville-replay-verify", "--pack", str(pack_path), "--ledger", str(ledger_path), "--out", str(replay_path)])
            replay = json.loads(replay_path.read_text(encoding="utf-8"))
        self.assertEqual(rc, 0)
        self.assertTrue(replay["replay_verified"])

    def test_cli_smallville_metrics(self) -> None:
        pair = build_baseline_intervention_pair(seed=20260517, ticks=12)
        with tempfile.TemporaryDirectory() as tmp:
            pack_path = Path(tmp) / "pack.json"
            baseline_path = Path(tmp) / "baseline.json"
            intervention_path = Path(tmp) / "intervention.json"
            delta_path = Path(tmp) / "delta.json"
            metrics_path = Path(tmp) / "metrics.json"
            pack_path.write_text(json.dumps(pair["pack"]), encoding="utf-8")
            baseline_path.write_text(json.dumps(pair["baseline"]), encoding="utf-8")
            intervention_path.write_text(json.dumps(pair["intervention"]), encoding="utf-8")
            delta_path.write_text(json.dumps(pair["delta"]), encoding="utf-8")
            rc = cli_main(
                [
                    "smallville-metrics",
                    "--pack",
                    str(pack_path),
                    "--baseline",
                    str(baseline_path),
                    "--intervention-run",
                    str(intervention_path),
                    "--delta",
                    str(delta_path),
                    "--out",
                    str(metrics_path),
                ]
            )
            metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        self.assertEqual(rc, 0)
        self.assertTrue(metrics["falsifiers"]["passed"])
        self.assertTrue(metrics["hash_chain_valid"])

    def test_metrics_and_falsifiers_pass(self) -> None:
        pair = build_baseline_intervention_pair(seed=20260517, ticks=12)
        replay = verify_replay(pair["baseline"], pair["pack"])
        falsifier = falsify_v0_2(pair["pack"], pair["baseline"], pair["intervention"], pair["delta"])
        metrics = build_metrics_v0_2(
            seed=20260517,
            pack=pair["pack"],
            baseline=pair["baseline"],
            intervention=pair["intervention"],
            delta=pair["delta"],
            replay=replay,
            falsifier=falsifier,
        )
        self.assertTrue(falsifier["passed"])
        self.assertEqual(metrics["agents"], 25)
        self.assertEqual(metrics["boundary"]["publication_gate"], "BLOCK")
        self.assertEqual(metrics["falsifiers"]["failed"], [])

    def test_cli_smallville_v02_report_writes_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            rc = cli_main(
                [
                    "smallville-v02-report",
                    "--ticks",
                    "12",
                    "--out-dir",
                    tmp,
                    "--out",
                    str(manifest_path),
                    "--pretty",
                ]
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(rc, 0)
        self.assertEqual(manifest["publication_gate"], "BLOCK")
        self.assertIn("pack", manifest["artifacts"])
        self.assertIn("report", manifest["artifacts"])


if __name__ == "__main__":
    unittest.main()
