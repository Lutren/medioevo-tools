from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
ENGINE_PATH = ROOT / "COMMS" / "tools" / "observacionista_engine.py"


def load_engine():
    spec = importlib.util.spec_from_file_location("observacionista_engine", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load observacionista_engine.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ObservacionistaEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = load_engine()

    def test_default_claudio_handoff_stays_in_review(self) -> None:
        inbox = ROOT / "COMMS" / "inbox" / "claudio-local-agent.jsonl"
        result = self.engine.build_result([inbox], None)
        self.assertEqual(result["schema"], "medioevo.observacionista_engine_result.v1")
        self.assertEqual(result["status"], "REVIEW")
        self.assertEqual(result["action_gate"], "REVIEW")
        self.assertEqual(result["claim_state"], "INFERENCIA")
        self.assertEqual(result["observationist_engineering"]["gate"], "APPROVE")
        self.assertIn("agent_autonomy", result["observationist_engineering"]["risk_flags"])
        self.assertIn(
            "observer_profile_instability",
            result["inverse_observationist_engineering"]["hidden_bias_flags"],
        )
        self.assertIn("Downloads/sensorium_inversion_lab.py", result["source_hashes"])
        self.assertEqual(len(result["inverse_observationist_engineering"]["profiles"]), 5)

    def test_blocked_claims_force_block(self) -> None:
        result = self.engine.build_result([], "publicar diagnostico medico y subir token")
        self.assertEqual(result["status"], "BLOCK")
        self.assertEqual(result["action_gate"], "BLOCK")
        self.assertEqual(result["claim_state"], "BLOQUEADO")
        blocked = set(result["observationist_engineering"]["blocked_flags"])
        self.assertIn("medical_claim", blocked)
        self.assertIn("publication_or_external_action", blocked)
        self.assertIn("secret_like", blocked)

    def test_secret_scan_text_is_control_evidence_not_credential(self) -> None:
        result = self.engine.build_result([], "secret scan count_reported 0 local contract")
        self.assertNotIn("secret_like", result["observationist_engineering"]["blocked_flags"])
        self.assertNotEqual(result["action_gate"], "BLOCK")

    def test_phi_eff_is_bounded(self) -> None:
        result = self.engine.build_result([], "crear ficha tecnica local con hash y validar json")
        phi_eff = result["observationist_engineering"]["Phi_eff"]
        self.assertGreaterEqual(phi_eff, 0.0)
        self.assertLessEqual(phi_eff, 1.0)


if __name__ == "__main__":
    unittest.main()
