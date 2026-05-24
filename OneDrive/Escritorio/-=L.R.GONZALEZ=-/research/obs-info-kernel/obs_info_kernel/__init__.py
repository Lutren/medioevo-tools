"""Observacionismo Research Kernel: anti-informacion + informacion oscura."""
from .core import Source, EstadoPSI, Finding
from .eor import EORCalculator
from .epistemic_guard import Claim, ClaimStatus, EpistemicGuard
from .equivalence import EquivalenceCheck, EquivalenceTester, EquivalenceVerdict
from .eml import EMLDomainError, EXPERIMENTAL_OPERATOR_STATUS, eml, gap_eml, operator_contract, residue_eml
from .hypothesis import Hypothesis, HypothesisScorer
from .math_canon import EML, MATH_CANON_VERSION, SCIENCE_CLAIM_GATE, R_noisy_or, classify_claim_math_status, phi_moi, validate_R_bounds
from .operator_profile import OperatorProfile, OperatorProfiler
from .orchestrator import ObservacionismoResearchKernel
from .topology import CijEdge, OperatorTopology

__all__ = [
    "Source",
    "EstadoPSI",
    "Finding",
    "ObservacionismoResearchKernel",
    "EORCalculator",
    "Claim",
    "ClaimStatus",
    "EpistemicGuard",
    "EquivalenceCheck",
    "EquivalenceTester",
    "EquivalenceVerdict",
    "eml",
    "residue_eml",
    "gap_eml",
    "operator_contract",
    "EMLDomainError",
    "EXPERIMENTAL_OPERATOR_STATUS",
    "MATH_CANON_VERSION",
    "SCIENCE_CLAIM_GATE",
    "R_noisy_or",
    "phi_moi",
    "EML",
    "validate_R_bounds",
    "classify_claim_math_status",
    "Hypothesis",
    "HypothesisScorer",
    "OperatorProfile",
    "OperatorProfiler",
    "CijEdge",
    "OperatorTopology",
]
__version__ = "0.1.0"
