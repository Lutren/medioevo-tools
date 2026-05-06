"""Metric observation primitives for public-safe agent perception.

This module turns the "sensors as metric axes" idea into a dependency-free
contract. It does not claim consciousness or physics validation. It only gives
agents a stable way to represent observations as calibrated vectors with
evidence, confidence and residue.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
import math
from typing import Any, Mapping, Sequence


SCHEMA_OBSERVATION_VECTOR = "obsai.metric_observation_vector.v1"
SCHEMA_CONSENSUS_OBSERVATION = "obsai.metric_consensus_observation.v1"


def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def _stable_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


@dataclass(frozen=True)
class MetricAxis:
    """One measurable axis in an observation vector."""

    name: str
    unit: str
    minimum: float = 0.0
    maximum: float = 1.0
    modality: str = "operational"
    description: str = ""

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("MetricAxis.name is required")
        if not math.isfinite(self.minimum) or not math.isfinite(self.maximum):
            raise ValueError("MetricAxis bounds must be finite")
        if self.maximum <= self.minimum:
            raise ValueError("MetricAxis.maximum must be greater than minimum")

    def normalize(self, raw_value: float) -> float:
        """Map a raw value into [0, 1] using the axis range."""

        return _clamp((float(raw_value) - self.minimum) / (self.maximum - self.minimum))


@dataclass(frozen=True)
class MetricSignal:
    """A measured event before it becomes an observation vector."""

    source: str
    modality: str
    metrics: Mapping[str, float]
    timestamp: float
    confidence: float = 1.0
    evidence_ref: str = ""
    periods: Mapping[str, float] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.source:
            raise ValueError("MetricSignal.source is required")
        if not self.modality:
            raise ValueError("MetricSignal.modality is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("MetricSignal.confidence must be in [0, 1]")
        for key, value in self.metrics.items():
            if not math.isfinite(float(value)):
                raise ValueError(f"MetricSignal metric {key!r} must be finite")
        for key, value in self.periods.items():
            if float(value) <= 0 or not math.isfinite(float(value)):
                raise ValueError(f"MetricSignal period {key!r} must be positive and finite")

    def with_derived_periods(self, frequency_suffix: str = "_hz") -> "MetricSignal":
        """Return a copy with periods derived from positive frequency metrics."""

        derived = dict(self.periods)
        for key, value in self.metrics.items():
            frequency = float(value)
            if key.endswith(frequency_suffix) and frequency > 0:
                derived.setdefault(key[: -len(frequency_suffix)] + "_period_s", 1.0 / frequency)
        return MetricSignal(
            source=self.source,
            modality=self.modality,
            metrics=dict(self.metrics),
            timestamp=self.timestamp,
            confidence=self.confidence,
            evidence_ref=self.evidence_ref,
            periods=derived,
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class MetricSensor:
    """Maps one signal metric into one normalized axis."""

    axis: MetricAxis
    metric_key: str
    accepted_modality: str | None = None
    sensitivity: float = 1.0

    def observe(self, signal: MetricSignal) -> float | None:
        if self.accepted_modality is not None and signal.modality != self.accepted_modality:
            return None
        if self.metric_key not in signal.metrics:
            return None
        raw = float(signal.metrics[self.metric_key]) * self.sensitivity
        return self.axis.normalize(raw)


@dataclass(frozen=True)
class ObservationVector:
    """Current agent observation over named metric axes."""

    axis_values: Mapping[str, float]
    axis_units: Mapping[str, str]
    source: str
    timestamp: float
    confidence: float
    residue: float
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    claim_level: str = "operational"
    schema_version: str = SCHEMA_OBSERVATION_VECTOR

    @property
    def axis_names(self) -> tuple[str, ...]:
        return tuple(sorted(self.axis_values))

    def aligned_values(self, axis_names: Sequence[str], fill: float = 0.0) -> tuple[float, ...]:
        return tuple(float(self.axis_values.get(axis, fill)) for axis in axis_names)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": self.schema_version,
            "source": self.source,
            "timestamp": self.timestamp,
            "claimLevel": self.claim_level,
            "confidence": round(float(self.confidence), 6),
            "residue": round(float(self.residue), 6),
            "axisValues": {key: round(float(self.axis_values[key]), 6) for key in self.axis_names},
            "axisUnits": {key: self.axis_units[key] for key in sorted(self.axis_units)},
            "evidenceRefs": list(self.evidence_refs),
        }

    def fingerprint(self) -> str:
        return sha256(_stable_json(self.to_dict()).encode("utf-8")).hexdigest()


class PhenomenalMetricSpace:
    """Mutable state space built from explicit sensors."""

    def __init__(self) -> None:
        self._sensors: dict[str, MetricSensor] = {}
        self._values: dict[str, float] = {}
        self._units: dict[str, str] = {}

    def add_sensor(self, sensor: MetricSensor) -> None:
        axis_name = sensor.axis.name
        if axis_name in self._sensors:
            raise ValueError(f"duplicate metric axis: {axis_name}")
        self._sensors[axis_name] = sensor
        self._values[axis_name] = 0.0
        self._units[axis_name] = sensor.axis.unit

    def update(self, signal: MetricSignal) -> ObservationVector:
        matched = 0
        for axis_name, sensor in self._sensors.items():
            value = sensor.observe(signal)
            if value is None:
                continue
            self._values[axis_name] = value
            matched += 1

        total = max(1, len(self._sensors))
        coverage = matched / total
        residue = 1.0 - coverage if matched else 1.0
        return ObservationVector(
            axis_values=dict(self._values),
            axis_units=dict(self._units),
            source=signal.source,
            timestamp=signal.timestamp,
            confidence=_clamp(signal.confidence * coverage),
            residue=_clamp(residue),
            evidence_refs=tuple(ref for ref in (signal.evidence_ref,) if ref),
        )

    def state(self, source: str = "metric_space", timestamp: float = 0.0) -> ObservationVector:
        return ObservationVector(
            axis_values=dict(self._values),
            axis_units=dict(self._units),
            source=source,
            timestamp=timestamp,
            confidence=1.0,
            residue=0.0,
        )


@dataclass(frozen=True)
class CalibrationProfile:
    """Maps local axis names into canonical names."""

    axis_aliases: Mapping[str, str] = field(default_factory=dict)
    axis_weights: Mapping[str, float] = field(default_factory=dict)

    def canonical_axis(self, axis_name: str) -> str:
        return self.axis_aliases.get(axis_name, axis_name)

    def weight(self, axis_name: str) -> float:
        return float(self.axis_weights.get(self.canonical_axis(axis_name), 1.0))

    def align(self, vector: ObservationVector) -> dict[str, float]:
        buckets: dict[str, list[float]] = {}
        for axis_name, value in vector.axis_values.items():
            canonical = self.canonical_axis(axis_name)
            buckets.setdefault(canonical, []).append(float(value) * self.weight(axis_name))
        return {axis: sum(values) / len(values) for axis, values in buckets.items()}


@dataclass(frozen=True)
class ConsensusObservation:
    """Consensus vector plus uncertainty residue across observers."""

    axis_values: Mapping[str, float]
    confidence: float
    residue: float
    contributors: int
    axis_coverage: Mapping[str, float]
    schema_version: str = SCHEMA_CONSENSUS_OBSERVATION

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": self.schema_version,
            "contributors": self.contributors,
            "confidence": round(float(self.confidence), 6),
            "residue": round(float(self.residue), 6),
            "axisValues": {key: round(float(self.axis_values[key]), 6) for key in sorted(self.axis_values)},
            "axisCoverage": {key: round(float(self.axis_coverage[key]), 6) for key in sorted(self.axis_coverage)},
        }


def build_consensus(
    vectors: Sequence[ObservationVector],
    calibration: CalibrationProfile | None = None,
) -> ConsensusObservation:
    """Build a residue-aware consensus without assuming identical dimensions."""

    if not vectors:
        raise ValueError("at least one ObservationVector is required")
    profile = calibration or CalibrationProfile()
    aligned = [profile.align(vector) for vector in vectors]
    axes = sorted({axis for row in aligned for axis in row})

    values: dict[str, float] = {}
    coverage: dict[str, float] = {}
    axis_residues: list[float] = []
    for axis in axes:
        present = [row[axis] for row in aligned if axis in row]
        mean = sum(present) / len(present)
        values[axis] = _clamp(mean)
        coverage[axis] = len(present) / len(aligned)
        if len(present) > 1:
            axis_residues.append(sum(abs(value - mean) for value in present) / len(present))
        axis_residues.append(1.0 - coverage[axis])

    confidence = sum(vector.confidence for vector in vectors) / len(vectors)
    mean_coverage = sum(coverage.values()) / max(1, len(coverage))
    residue = sum(axis_residues) / max(1, len(axis_residues))
    return ConsensusObservation(
        axis_values=values,
        confidence=_clamp(confidence * mean_coverage),
        residue=_clamp(residue),
        contributors=len(vectors),
        axis_coverage=coverage,
    )


@dataclass
class MetaObservationLayer:
    """Attention layer that reflects over observation vectors."""

    attention_weights: dict[str, float] = field(default_factory=dict)

    def focus_attention(self, axis_name: str, weight: float = 1.5) -> None:
        if weight <= 0 or not math.isfinite(weight):
            raise ValueError("attention weight must be positive and finite")
        self.attention_weights[axis_name] = float(weight)

    def reflect(self, vector: ObservationVector) -> dict[str, Any]:
        weighted = {
            axis: _clamp(float(value) * self.attention_weights.get(axis, 1.0))
            for axis, value in vector.axis_values.items()
        }
        focus_axis = max(weighted, key=weighted.get) if weighted else None
        return {
            "schemaVersion": "obsai.metric_meta_observation.v1",
            "source": vector.source,
            "focusAxis": focus_axis,
            "weightedAxisValues": {key: round(weighted[key], 6) for key in sorted(weighted)},
            "confidence": round(vector.confidence, 6),
            "residue": round(vector.residue, 6),
            "claimBoundary": "operational_vector_not_consciousness_claim",
        }
