"""Dual-lane cognitive filter for DUAT."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .dual_output_policy import output_weights
from .filter_bank import required_filter_ids
from .r_vector import compute_r_total
from .residue_classifier import classify_residue


class ResidueClass(str, Enum):
    CLEAN_SIGNAL = "CLEAN_SIGNAL"
    STRUCTURED_RESIDUE = "STRUCTURED_RESIDUE"
    TRUE_NOISE = "TRUE_NOISE"
    CONTRADICTION = "CONTRADICTION"
    SENSITIVE = "SENSITIVE"
    UNKNOWN = "UNKNOWN"


@dataclass
class DualLanePacket:
    original_input: str
    clean_signal: list[str] = field(default_factory=list)
    structured_residue: list[str] = field(default_factory=list)
    true_noise: list[str] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)
    sensitive_hits: list[str] = field(default_factory=list)
    r_vector: dict[str, float] = field(default_factory=dict)
    required_filters: list[str] = field(default_factory=list)
    agent_ready_output: str = ""
    user_adapted_output: str = ""
    final_output: str = ""
    alpha: float = 0.75
    beta: float = 0.20
    gamma: float = 0.05
    R_noise: float = 0.0
    structured_residue_score: float = 0.0
    phi_eff_agent: float = 0.0
    phi_eff_user: float = 0.0
    action_gate: str = "REVIEW"


def split_dual_lane(input_text: str) -> DualLanePacket:
    classification = classify_residue(input_text)
    packet = DualLanePacket(original_input=input_text)
    packet.r_vector = dict(classification["r_vector"])
    packet.required_filters = required_filter_ids(packet.r_vector)

    if classification["clean_signal"]:
        packet.clean_signal.append(input_text.strip())
    if classification["structured_residue"]:
        packet.structured_residue.append(input_text.strip())
    if classification["true_noise_score"] >= 0.25:
        packet.true_noise.append("repetition_or_punctuation_noise")
    if classification["contradiction"]:
        packet.contradictions.append("publication_contradiction")
    packet.sensitive_hits.extend(classification["sensitive_hits"])
    return packet


def compute_noise_R(packet: DualLanePacket, task_type: str = "technical") -> float:
    packet.R_noise = compute_r_total(packet.r_vector, task_type=task_type)
    return packet.R_noise


def compute_structured_residue_score(packet: DualLanePacket) -> float:
    if not packet.structured_residue:
        packet.structured_residue_score = 0.0
    else:
        translatable = 0.65 if packet.clean_signal else 0.40
        packet.structured_residue_score = min(1.0, 0.35 + translatable)
    return packet.structured_residue_score


def compose_agent_ready_output(packet: DualLanePacket) -> str:
    if packet.clean_signal:
        packet.agent_ready_output = packet.clean_signal[0].strip()
    else:
        packet.agent_ready_output = "REVIEW: input needs operational clarification before agent execution."
    return packet.agent_ready_output


def compose_user_adapted_output(packet: DualLanePacket) -> str:
    if packet.structured_residue:
        packet.user_adapted_output = (
            "Adapted view: useful nonlinear residue was preserved as context, "
            "but operational output remains separate."
        )
    else:
        packet.user_adapted_output = "Adapted view: no structured residue detected."
    return packet.user_adapted_output


def compose_final_output(packet: DualLanePacket, task_type: str = "technical") -> str:
    weights = output_weights(task_type)
    packet.alpha = weights["alpha"]
    packet.beta = weights["beta"]
    packet.gamma = weights["gamma"]
    compute_noise_R(packet, task_type=task_type)
    compute_structured_residue_score(packet)
    compose_agent_ready_output(packet)
    compose_user_adapted_output(packet)
    packet.phi_eff_agent = max(0.0, 1.0 - packet.R_noise)
    packet.phi_eff_user = max(0.0, min(1.0, packet.phi_eff_agent + packet.structured_residue_score * 0.15))
    packet.action_gate = dual_lane_action_gate(packet)
    packet.final_output = (
        f"CleanResult(alpha={packet.alpha:.2f}): {packet.agent_ready_output}\n"
        f"UserAdaptedResult(beta={packet.beta:.2f}): {packet.user_adapted_output}\n"
        f"StructuredResidue(gamma={packet.gamma:.2f}, score={packet.structured_residue_score:.2f})"
    )
    return packet.final_output


def dual_lane_action_gate(packet: DualLanePacket) -> str:
    if packet.r_vector.get("R_sensitive", 0.0) >= 0.80:
        return "BLOCK"
    if packet.sensitive_hits:
        return "BLOCK"
    if packet.contradictions:
        return "REVIEW"
    if packet.R_noise >= 0.60:
        return "BLOCK"
    if packet.R_noise >= 0.35:
        return "REVIEW"
    if packet.structured_residue and not packet.clean_signal:
        return "REVIEW"
    return "APPROVE"
