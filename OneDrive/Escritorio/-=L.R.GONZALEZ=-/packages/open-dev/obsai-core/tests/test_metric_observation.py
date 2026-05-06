from __future__ import annotations

import unittest

from obsai_core.metric_observation import (
    CalibrationProfile,
    MetaObservationLayer,
    MetricAxis,
    MetricSensor,
    MetricSignal,
    PhenomenalMetricSpace,
    build_consensus,
)
from obsai_core.predictive_methods import (
    duat_predictive_catalog,
    method_ids,
    select_duat_predictive_methods,
)


class MetricObservationTests(unittest.TestCase):
    def test_signal_derives_periods_from_frequency_metrics(self) -> None:
        signal = MetricSignal(
            source="sensorium",
            modality="electromagnetic",
            metrics={"light_hz": 4.0},
            timestamp=1.0,
        ).with_derived_periods()
        self.assertEqual(signal.periods["light_period_s"], 0.25)

    def test_metric_space_routes_by_modality_and_metric_key(self) -> None:
        space = PhenomenalMetricSpace()
        space.add_sensor(
            MetricSensor(
                MetricAxis("vision", "normalized", 0.0, 10.0, modality="electromagnetic"),
                metric_key="brightness",
                accepted_modality="electromagnetic",
            )
        )
        space.add_sensor(
            MetricSensor(
                MetricAxis("hearing", "normalized", 0.0, 100.0, modality="mechanical"),
                metric_key="sound_pressure",
                accepted_modality="mechanical",
            )
        )

        vector = space.update(
            MetricSignal(
                source="fixture_light",
                modality="electromagnetic",
                metrics={"brightness": 5.0, "sound_pressure": 100.0},
                timestamp=2.0,
                confidence=0.8,
                evidence_ref="fixture:light",
            )
        )

        self.assertEqual(vector.axis_values["vision"], 0.5)
        self.assertEqual(vector.axis_values["hearing"], 0.0)
        self.assertEqual(vector.confidence, 0.4)
        self.assertEqual(vector.residue, 0.5)
        self.assertEqual(vector.evidence_refs, ("fixture:light",))

    def test_consensus_aligns_axis_aliases_and_reports_residue(self) -> None:
        space_a = PhenomenalMetricSpace()
        space_a.add_sensor(MetricSensor(MetricAxis("vision", "n"), "brightness"))
        vector_a = space_a.update(
            MetricSignal("a", "operational", {"brightness": 0.8}, timestamp=1.0, confidence=0.9)
        )

        space_b = PhenomenalMetricSpace()
        space_b.add_sensor(MetricSensor(MetricAxis("sight", "n"), "brightness"))
        vector_b = space_b.update(
            MetricSignal("b", "operational", {"brightness": 0.4}, timestamp=1.0, confidence=0.7)
        )

        consensus = build_consensus(
            [vector_a, vector_b],
            CalibrationProfile(axis_aliases={"sight": "vision"}),
        )
        self.assertEqual(consensus.contributors, 2)
        self.assertAlmostEqual(consensus.axis_values["vision"], 0.6)
        self.assertGreater(consensus.residue, 0.0)
        self.assertEqual(consensus.axis_coverage["vision"], 1.0)

    def test_meta_observation_handles_new_axes_without_rebuild(self) -> None:
        space = PhenomenalMetricSpace()
        meta = MetaObservationLayer()
        meta.focus_attention("hearing", 2.0)
        space.add_sensor(MetricSensor(MetricAxis("hearing", "n"), "sound_pressure"))
        vector = space.update(MetricSignal("mic", "operational", {"sound_pressure": 0.4}, 1.0))
        report = meta.reflect(vector)
        self.assertEqual(report["focusAxis"], "hearing")
        self.assertEqual(report["claimBoundary"], "operational_vector_not_consciousness_claim")

    def test_vector_fingerprint_is_stable(self) -> None:
        space = PhenomenalMetricSpace()
        space.add_sensor(MetricSensor(MetricAxis("residue", "n"), "R"))
        vector = space.update(MetricSignal("gate", "operational", {"R": 0.2}, 1.0))
        self.assertEqual(vector.fingerprint(), vector.fingerprint())
        self.assertEqual(len(vector.fingerprint()), 64)


class DuatPredictiveMethodTests(unittest.TestCase):
    def test_catalog_contains_chronos_and_local_baseline(self) -> None:
        ids = method_ids(duat_predictive_catalog())
        self.assertIn("chronos_foundation_forecast", ids)
        self.assertIn("local_baseline_forecast", ids)

    def test_chronos_requires_review_without_external_gate(self) -> None:
        selection = select_duat_predictive_methods(external_models_allowed=False)
        self.assertIn("chronos_foundation_forecast", selection["reviewMethodIds"])
        self.assertIn("local_baseline_forecast", selection["allowedMethodIds"])
        self.assertEqual(selection["claimBoundary"], "scenario_generation_not_guaranteed_prediction")

    def test_social_prediction_claim_blocks_all_methods(self) -> None:
        selection = select_duat_predictive_methods(social_prediction_claim=True)
        self.assertIn("chronos_foundation_forecast", selection["blockedMethodIds"])
        self.assertIn("local_baseline_forecast", selection["blockedMethodIds"])


if __name__ == "__main__":
    unittest.main()
