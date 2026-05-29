"""WS2: DUAT Genesis classifies observations and blocks on BLOQUEADO via obsai-core."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from duat_genesis import (
    Observation,
    classify_observation,
    fingerprint_handoff,
    gate_observations,
    run_simulation,
    validate_and_fingerprint,
)


class ObsaiBridgeTests(unittest.TestCase):
    def test_benign_default_observation_is_not_blocked(self) -> None:
        run = run_simulation(seed="demo", size=6, ticks=2)
        self.assertEqual(run.claims["observation_gate"], "APPROVE")

    def test_low_confidence_observation_classifies_bloqueado(self) -> None:
        obs = Observation(observer_id="x", target_index=0, signal=0.1, confidence=0.2)
        self.assertEqual(classify_observation(obs), "BLOQUEADO")  # residue 0.8 -> JAMMING

    def test_explicit_bloqueado_observation_blocks_simulation(self) -> None:
        obs = (
            Observation(
                observer_id="x",
                target_index=0,
                signal=0.1,
                confidence=1.0,
                metadata={"epistemic_state": "BLOQUEADO"},
            ),
        )
        with self.assertRaises(ValueError):
            run_simulation(seed="demo", size=4, ticks=1, observations=obs)

    def test_hard_boundary_tag_blocks_simulation(self) -> None:
        obs = (
            Observation(
                observer_id="x",
                target_index=0,
                signal=0.1,
                confidence=0.9,
                metadata={"policy_tags": ["secret"]},
            ),
        )
        with self.assertRaises(ValueError):
            run_simulation(seed="demo", size=4, ticks=1, observations=obs)

    def test_block_on_jamming_false_records_block_but_runs(self) -> None:
        obs = (Observation(observer_id="x", target_index=0, signal=0.1, confidence=0.2),)
        run = run_simulation(seed="demo", size=4, ticks=1, observations=obs, block_on_jamming=False)
        self.assertEqual(run.claims["observation_gate"], "BLOCK")

    def test_gate_observations_reports_states(self) -> None:
        good = Observation(observer_id="g", target_index=0, signal=0.1, confidence=0.95)
        bad = Observation(observer_id="b", target_index=0, signal=0.1, confidence=0.2)
        gate = gate_observations([good, bad])
        self.assertTrue(gate["blocked"])
        self.assertEqual(gate["states"][0], "CERTEZA")
        self.assertEqual(gate["states"][1], "BLOQUEADO")

    def test_handoff_fingerprint_is_stable_and_64_hex(self) -> None:
        text = "ESTADO CERTEZA INFERENCIA INCOGNITA ACCION ARTEFACTO HANDOFF NEXT FINGERPRINT"
        first = fingerprint_handoff(text)
        second = fingerprint_handoff(text)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)
        stamped = validate_and_fingerprint(text)
        self.assertEqual(stamped["fingerprint"], first)
        self.assertTrue(stamped["ok"])


if __name__ == "__main__":
    unittest.main()
