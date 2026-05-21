"""
ClaimClassifier — obsai_core.claim_classifier
==============================================
Cerebro #2.1: atomiza texto → clasifica claims → aplica gates → emite ObservationEnvelope.

Pipeline:
    texto_bruto
        → atomize()          split en claims atómicos
        → classify()         CERTEZA / INFERENCIA / INCOGNITA / BLOQUEO
        → _c_gate()          claridad C ≥ 0.60
        → _science_gate()    física/AGI/consciencia = BLOQUEO
        → _compute_r()       R_or desde componentes r_src, r_def, r_tst, r_bnd
        → _phi_moi()         (T·S·C·K·(1-R))^(1/5)
        → ObservationEnvelope

Etiquetado epistémico (canónico — CLAUDE.md + 07b §2):
    CERTEZA   — demostrable, verificable, falsificable; soporte empírico fuerte
    INFERENCIA — plausible, basado en evidencia parcial; puede estar equivocado
    INCOGNITA  — sin evidencia suficiente; se marca sin afirmar
    BLOQUEO    — viola ScienceClaimGate (física nueva, AGI, consciencia, medicina)
                  o el sistema no tiene capacidad epistémica para evaluarlo

Claim calibration: DEMO_ONLY
Thresholds: DEMO_ONLY — no son afirmaciones científicas validadas.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

from .metrics import clamp01

# ---------------------------------------------------------------------------
# Tipos
# ---------------------------------------------------------------------------

EpistemicLabel = Literal["CERTEZA", "INFERENCIA", "INCOGNITA", "BLOQUEO"]
GateDecision = Literal["APPROVE", "REVIEW", "BLOCK"]

# ---------------------------------------------------------------------------
# Patrones de clasificación
# ---------------------------------------------------------------------------

# Señales de CERTEZA — lógica formal, aritmética, identidades verificables
_CERTEZA_PATTERNS: list[str] = [
    r"\b(es igual a|equals|=|≡|por definición|by definition|demostrad[oa]|proven|verificad[oa]|verified)\b",
    r"\b(siempre|always|nunca|never|todo|all|ningún|none)\b.*\b(matemáticamente|matemática|math|lógicamente|logically)\b",
    r"\b(fórmula|formula|ecuación|equation|teorema|theorem|prueba|proof)\b",
    r"\d+\s*[\+\-\*\/]\s*\d+\s*=\s*\d+",  # aritmética explícita
    # Hechos empíricos con unidades verificables
    r"\d+\s*°[CF]",                         # temperatura con grado
    r"\d+\s*(kg|km|m|cm|mm|nm|atm|pa|bar|mol|J|W|Hz|nm|eV)\b",  # magnitud + unidad
    r"\b(al nivel del mar|at sea level|en condiciones normales|at STP)\b",
]

# Señales de INFERENCIA — probabilidad, tendencia, correlación
_INFERENCIA_PATTERNS: list[str] = [
    r"\b(probablemente|probably|likely|parece|seems|sugiere|suggests|indica|indicates)\b",
    r"\b(podría|could|might|may|puede que|perhaps|quizás|possibly)\b",
    r"\b(correlaciona|correlates|asocia|associated|tiende a|tends to)\b",
    r"\b(evidencia|evidence|dato|data|estudio|study|observación|observation)\b.*\b(sugiere|indica|apunta)\b",
    r"\b(en general|generally|usualmente|usually|a menudo|often)\b",
    r"\b(según|de acuerdo con|according to|based on|basado en|conforme a)\b",
    r"\b(mejora|improves?|aumenta|increases?|reduce[sd]?|disminuye)\b.*\b(la|el|los|las|the)\b",
]

# Señales de BLOQUEO — ScienceClaimGate (07b §safeboundary)
_BLOQUEO_PATTERNS: list[str] = [
    # Física especulativa
    r"\b(nueva física|new physics|beyond standard model|más allá del modelo estándar)\b",
    r"\b(dimensión(es)? extra|extra dimension|multiverso|multiverse|universo paralelo)\b",
    r"\b(viaje en el tiempo|time travel|taquión|tachyon|energía oscura causa|dark energy causes)\b",
    r"\b(modifica(r)? la gravedad|modify gravity|nueva teoría de todo|new theory of everything)\b",
    # AGI / consciencia
    r"\b(AGI|inteligencia artificial general|superinteligencia|superintelligence)\b.*\b(es|está|será|will be)\b",
    r"\b(la IA (es|tiene|siente)|AI (is conscious|has feelings|is sentient))\b",
    r"\b(consciencia (emerge|is|=)|consciousness (emerges from|equals))\b",
    r"\b(Phi\s*[><=]\s*0.*consciencia|integrated information.*proves)\b",
    # Medicina sin evidencia
    r"\b(cura(r)?|cure|trata(r)?|treats?|previene|prevents?)\b.*\b(cáncer|cancer|diabetes|alzheimer|covid)\b",
    r"\b(garantiza(r)?|guarantees?)\b.*\b(salud|health|longevidad|longevity)\b",
]

# Dominios con ScienceClaimGate automático
_SCIENCE_GATE_DOMAINS: list[str] = [
    "física especulativa", "speculative physics",
    "consciencia", "consciousness", "qualia",
    "agi", "superinteligencia", "superintelligence",
    "medicina", "medical", "cura", "cure",
    "predicción garantizada", "guaranteed prediction",
]

# Señales de baja claridad (C < 0.60)
_LOW_CLARITY_PATTERNS: list[str] = [
    r"\b(esto|it|eso|ello|aquello)\b(?!\s+\w{4,})",  # pronombre sin referente claro
    r"\.\.\.$",  # oración incompleta
    r"^[A-ZÁÉÍÓÚ][a-záéíóú]+\s*$",  # una sola palabra
    r"\b(etc|etc\.|y más|and more|entre otros|among others)\b$",  # cierre vago
]

# ---------------------------------------------------------------------------
# Dataclasses de output
# ---------------------------------------------------------------------------

@dataclass
class RComponents:
    """Componentes del residuo (ver 07b §2 fórmula R_or = 1 − Π(1−r_i))."""
    r_src: float = 0.0   # fuentes ausentes o no verificadas
    r_def: float = 0.0   # definición vaga o ambigua
    r_tst: float = 0.0   # no tiene falsificador o test
    r_bnd: float = 0.0   # viola boundary (ScienceClaimGate)

    def r_or(self) -> float:
        """R_or = 1 − Π(1−r_i)  — CERTEZA matemática (07b §2)."""
        product = 1.0
        for r in (self.r_src, self.r_def, self.r_tst, self.r_bnd):
            product *= (1.0 - clamp01(r))
        return clamp01(1.0 - product)


@dataclass
class ClaimResult:
    """Resultado de clasificar un claim atómico."""
    text: str
    label: EpistemicLabel
    clarity: float          # C ∈ [0,1]
    R_components: RComponents
    R_or: float
    phi_moi: float          # (T·S·C·K·(1-R))^(1/5) — DEMO_ONLY thresholds
    gate: GateDecision
    falsifier_hint: str | None = None
    rewrite_hint: str | None = None
    science_gate_triggered: bool = False
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "label": self.label,
            "clarity": round(self.clarity, 3),
            "R_components": {
                "r_src": round(self.R_components.r_src, 3),
                "r_def": round(self.R_components.r_def, 3),
                "r_tst": round(self.R_components.r_tst, 3),
                "r_bnd": round(self.R_components.r_bnd, 3),
            },
            "R_or": round(self.R_or, 3),
            "phi_moi": round(self.phi_moi, 3),
            "gate": self.gate,
            "falsifier_hint": self.falsifier_hint,
            "rewrite_hint": self.rewrite_hint,
            "science_gate_triggered": self.science_gate_triggered,
            "warnings": self.warnings,
        }


@dataclass
class ObservationEnvelope:
    """
    Envelope v2.1 — output universal de cualquier cerebro.
    Schema completo en: 02_METODO_MOI/02_OBSERVATION_ENVELOPE_SCHEMA.yaml
    """
    agent: str
    task: str
    timestamp: str
    claims: list[ClaimResult]
    R_or: float
    phi_moi: float
    gate: GateDecision
    regime: Literal["EXPAND", "COMPRESS", "HOLD", "BLOCK"]
    evidence: list[str]
    falsifier: str | None
    next_action: str

    def to_dict(self) -> dict:
        return {
            "schemaVersion": "obsai.observation_envelope.v2.1",
            "agent": self.agent,
            "task": self.task,
            "timestamp": self.timestamp,
            "claims": [c.to_dict() for c in self.claims],
            "R_or": round(self.R_or, 3),
            "phi_moi": round(self.phi_moi, 3),
            "gate": self.gate,
            "regime": self.regime,
            "evidence": self.evidence,
            "falsifier": self.falsifier,
            "next_action": self.next_action,
            "calibration": "DEMO_ONLY",
        }

# ---------------------------------------------------------------------------
# ClaimClassifier
# ---------------------------------------------------------------------------

class ClaimClassifier:
    """
    Cerebro modular #2.1: clasifica claims epistémicos sin dependencias externas.

    Uso básico::

        cc = ClaimClassifier()
        envelope = cc.classify("El agua hierve a 100°C al nivel del mar.")
        print(envelope.gate)  # APPROVE

    Parámetros de calibración (DEMO_ONLY):
        clarity_threshold : float — mínimo C para no marcar como REVIEW (default 0.60)
        r_src_base        : float — residuo base por ausencia de fuentes citadas (0.20)
    """

    CLARITY_THRESHOLD = 0.60  # C-GATE: C < threshold → REVIEW
    R_SRC_BASE = 0.20         # residuo base por claim sin fuente citada
    PHI_THRESHOLD_APPROVE = 0.55  # DEMO_ONLY

    # Indicadores de fuente explícita
    _SOURCE_PATTERNS: list[str] = [
        r"\(.*\d{4}.*\)",        # cita parentética (Autor 2023)
        r"\[.*\d+.*\]",          # cita numérica [1]
        r"https?://\S+",         # URL
        r"\b(según|according to|cita|cited in|referencia|ref\.)\b",
        r"\b(estudio|study|paper|publicación|publication|artículo|article)\b",
    ]

    def __init__(
        self,
        clarity_threshold: float = CLARITY_THRESHOLD,
        r_src_base: float = R_SRC_BASE,
        agent_name: str = "ClaimClassifier",
    ):
        self.clarity_threshold = clamp01(clarity_threshold)
        self.r_src_base = clamp01(r_src_base)
        self.agent_name = agent_name

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def classify(self, text: str, task: str = "claim_classification") -> ObservationEnvelope:
        """
        Clasifica texto completo: atomiza → clasifica cada claim → emite envelope.

        Args:
            text: Texto libre con uno o más claims.
            task: Descripción de la tarea (para el envelope).

        Returns:
            ObservationEnvelope con todos los claims clasificados y métricas agregadas.
        """
        atoms = self.atomize(text)
        results = [self._classify_atom(atom) for atom in atoms]
        return self._build_envelope(results, task)

    def classify_atom(self, text: str) -> ClaimResult:
        """Clasifica un solo claim atómico (sin atomizar)."""
        return self._classify_atom(text.strip())

    def atomize(self, text: str) -> list[str]:
        """
        Divide texto en claims atómicos (una idea por claim).

        Estrategia: split por punto/punto y coma/dos puntos seguido de mayúscula.
        Filtra fragmentos vacíos o demasiado cortos.
        """
        # Dividir por: '. ', '.\n', '; ', '? ', '! '
        parts = re.split(r"(?<=[.;?!])\s+(?=[A-ZÁÉÍÓÚÜÑ\"])|(?<=\n)(?=[A-ZÁÉÍÓÚÜÑ\"])", text)
        atoms: list[str] = []
        for part in parts:
            part = part.strip().rstrip(".")
            if len(part) >= 8:  # mínimo 8 chars para ser claim
                atoms.append(part)
        return atoms if atoms else [text.strip()]

    # ------------------------------------------------------------------
    # Pipeline interno
    # ------------------------------------------------------------------

    def _classify_atom(self, atom: str) -> ClaimResult:
        atom_lower = atom.lower()
        warnings: list[str] = []

        # 1. ScienceClaimGate — antes que todo
        science_triggered, science_reason = self._science_gate(atom_lower)
        if science_triggered:
            r_comp = RComponents(r_src=0.40, r_def=0.30, r_tst=0.60, r_bnd=0.90)
            r_or = r_comp.r_or()
            phi = self._phi_moi(T=0.1, S=0.1, C=0.1, K=0.1, R=r_or)
            return ClaimResult(
                text=atom,
                label="BLOQUEO",
                clarity=0.10,
                R_components=r_comp,
                R_or=r_or,
                phi_moi=phi,
                gate="BLOCK",
                falsifier_hint=None,
                rewrite_hint=f"ScienceClaimGate: {science_reason}. Reformula como INCOGNITA o elimina.",
                science_gate_triggered=True,
                warnings=[f"ScienceClaimGate activado: {science_reason}"],
            )

        # 2. Claridad (C-GATE)
        clarity = self._compute_clarity(atom)
        if clarity < self.clarity_threshold:
            warnings.append(f"C-GATE: claridad {clarity:.2f} < umbral {self.clarity_threshold:.2f}")

        # 3. Label epistémico
        label = self._label(atom_lower)

        # 4. Componentes de residuo
        r_comp = self._compute_r(atom_lower, label, clarity)
        r_or = r_comp.r_or()

        # 5. Phi_moi — DEMO_ONLY thresholds
        # T=transferabilidad, S=selectividad, C=claridad, K=conocimiento_soporte
        T = 0.80 if label == "CERTEZA" else (0.60 if label == "INFERENCIA" else 0.30)
        S = 0.70 if self._has_source(atom) else 0.40
        K = 0.85 if label == "CERTEZA" else (0.55 if label == "INFERENCIA" else 0.20)
        phi = self._phi_moi(T=T, S=S, C=clarity, K=K, R=r_or)

        # 6. Gate
        gate, gate_reason = self._gate(label, clarity, r_or, phi)
        if gate_reason:
            warnings.append(gate_reason)

        # 7. Hints
        falsifier = self._falsifier_hint(label, atom)
        rewrite = self._rewrite_hint(label, clarity, atom) if gate != "APPROVE" else None

        return ClaimResult(
            text=atom,
            label=label,
            clarity=clarity,
            R_components=r_comp,
            R_or=r_or,
            phi_moi=phi,
            gate=gate,
            falsifier_hint=falsifier,
            rewrite_hint=rewrite,
            science_gate_triggered=False,
            warnings=warnings,
        )

    def _label(self, text_lower: str) -> EpistemicLabel:
        """Clasifica el label epistémico por coincidencia de patrones."""
        # BLOQUEO primero (ya lo maneja _science_gate, pero por si acaso)
        for pattern in _BLOQUEO_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return "BLOQUEO"
        # CERTEZA
        for pattern in _CERTEZA_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return "CERTEZA"
        # INFERENCIA
        for pattern in _INFERENCIA_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return "INFERENCIA"
        # Default: INCOGNITA (sin señales suficientes)
        return "INCOGNITA"

    def _science_gate(self, text_lower: str) -> tuple[bool, str]:
        """ScienceClaimGate: retorna (triggered, reason)."""
        for pattern in _BLOQUEO_PATTERNS:
            m = re.search(pattern, text_lower, re.IGNORECASE)
            if m:
                return True, f"patrón detectado: '{m.group(0)}'"
        return False, ""

    def _compute_clarity(self, text: str) -> float:
        """
        C ∈ [0,1] — evalúa claridad léxica del claim.
        Penaliza: pronombres sin referente, oraciones incompletas, longitud mínima.
        DEMO_ONLY thresholds.
        """
        score = 1.0
        text_lower = text.lower()

        # Longitud mínima
        words = text.split()
        if len(words) < 3:
            score -= 0.40
        elif len(words) < 6:
            score -= 0.15

        # Patrones de baja claridad
        for pattern in _LOW_CLARITY_PATTERNS:
            if re.search(pattern, text_lower):
                score -= 0.12

        # Verbos epistémicos vagos sin referente
        vague = re.findall(r"\b(es bueno|is good|es malo|is bad|es importante|is important)\b", text_lower)
        score -= 0.10 * len(vague)

        return clamp01(score)

    def _has_source(self, text: str) -> bool:
        """True si el claim cita una fuente explícita."""
        for pattern in self._SOURCE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def _compute_r(self, text_lower: str, label: EpistemicLabel, clarity: float) -> RComponents:
        """
        Calcula componentes de residuo.
        Valores calibrados: DEMO_ONLY.
        """
        # r_src — ausencia de fuente
        r_src = 0.0 if self._has_source(text_lower) else self.r_src_base

        # r_def — vaguedad definicional
        r_def = clamp01(1.0 - clarity) * 0.60

        # r_tst — ausencia de falsificador evidente
        has_falsifier = bool(re.search(
            r"\b(si|if|cuando|when|excepto|except|a menos que|unless|falsif|test|verif)\b",
            text_lower
        ))
        r_tst = 0.0 if has_falsifier else (0.10 if label == "CERTEZA" else 0.30 if label == "INFERENCIA" else 0.50)

        # r_bnd — violación de boundary
        r_bnd = 0.0  # Si llegamos aquí, science_gate no disparó

        return RComponents(r_src=r_src, r_def=r_def, r_tst=r_tst, r_bnd=r_bnd)

    def _phi_moi(self, T: float, S: float, C: float, K: float, R: float) -> float:
        """
        Φ_moi = (T · S · C · K · (1−R))^(1/5)
        Fórmula canónica: 07b §2. Thresholds: DEMO_ONLY.
        """
        product = clamp01(T) * clamp01(S) * clamp01(C) * clamp01(K) * clamp01(1.0 - R)
        return clamp01(product ** (1.0 / 5.0))

    def _gate(
        self, label: EpistemicLabel, clarity: float, R_or: float, phi: float
    ) -> tuple[GateDecision, str]:
        """Decide APPROVE / REVIEW / BLOCK basado en label, claridad, R y Phi_moi."""
        if label == "BLOQUEO":
            return "BLOCK", "label=BLOQUEO"
        if R_or >= 0.70:
            return "BLOCK", f"R_or={R_or:.2f} ≥ 0.70"
        if clarity < self.clarity_threshold:
            return "REVIEW", f"C-GATE: claridad={clarity:.2f} < {self.clarity_threshold:.2f}"
        if label == "INCOGNITA" and R_or >= 0.45:
            return "REVIEW", f"INCOGNITA con R_or={R_or:.2f}"
        if phi < self.PHI_THRESHOLD_APPROVE:
            return "REVIEW", f"phi_moi={phi:.2f} < {self.PHI_THRESHOLD_APPROVE:.2f}"
        return "APPROVE", ""

    def _falsifier_hint(self, label: EpistemicLabel, text: str) -> str | None:
        """Sugiere un falsificador mínimo si el claim no lo tiene implícito."""
        if label == "CERTEZA":
            return "Verificable directamente: busca contraejemplo o condición donde falla."
        if label == "INFERENCIA":
            return "¿Qué observación demostraría que esta inferencia es incorrecta?"
        if label == "INCOGNITA":
            return "¿Qué dato o experimento podría resolver esta incógnita?"
        return None  # BLOQUEO — no aplica

    def _rewrite_hint(self, label: EpistemicLabel, clarity: float, text: str) -> str | None:
        """Sugerencia de reescritura si gate no es APPROVE."""
        if clarity < self.clarity_threshold:
            return f"Añade referente explícito y especifica el sujeto. Texto actual parece incompleto o vago."
        if label == "INCOGNITA":
            return f"Reformula como: 'Aún no se sabe si [claim] porque [razón].'"
        if label == "INFERENCIA":
            return f"Añade: 'Según [fuente/evidencia], se infiere que [claim]' para reducir R."
        return None

    # ------------------------------------------------------------------
    # Envelope builder
    # ------------------------------------------------------------------

    def _build_envelope(self, results: list[ClaimResult], task: str) -> ObservationEnvelope:
        """Agrega resultados de claims individuales en un ObservationEnvelope."""
        if not results:
            r_agg = 0.50
            phi_agg = 0.20
            gate_agg: GateDecision = "REVIEW"
            regime = "HOLD"
        else:
            # R_or agregado: OR ruidoso sobre todos los claims (07b §2)
            r_agg = clamp01(1.0 - (
                1.0 - sum(r.R_or for r in results) / len(results)
            ))
            phi_agg = sum(r.phi_moi for r in results) / len(results)

            # Gate: el más restrictivo gana
            if any(r.gate == "BLOCK" for r in results):
                gate_agg = "BLOCK"
            elif any(r.gate == "REVIEW" for r in results):
                gate_agg = "REVIEW"
            else:
                gate_agg = "APPROVE"

            # Régimen desde R_or agregado
            if r_agg < 0.20:
                regime = "EXPAND"
            elif r_agg < 0.45:
                regime = "COMPRESS"
            elif r_agg < 0.70:
                regime = "HOLD"
            else:
                regime = "BLOCK"

        # Evidencia — claims que pasaron APPROVE
        evidence = [
            f"claim[{i}]: {r.text[:60]}... → {r.label} ({r.gate})"
            for i, r in enumerate(results)
            if r.gate == "APPROVE"
        ] or ["ningún claim alcanzó gate APPROVE"]

        # Falsificador del claim con menor R
        best = min(results, key=lambda r: r.R_or) if results else None
        falsifier = best.falsifier_hint if best else None

        # Next action
        if gate_agg == "BLOCK":
            next_action = "Revisar claims bloqueados (BLOQUEO/ScienceGate). No proceder hasta resolver."
        elif gate_agg == "REVIEW":
            next_action = "Revisar claims en REVIEW: añadir fuentes, aumentar claridad o reformular."
        else:
            next_action = "Claims aprobados. Proceder con siguiente etapa del pipeline MOI."

        return ObservationEnvelope(
            agent=self.agent_name,
            task=task,
            timestamp=datetime.now(timezone.utc).isoformat(),
            claims=results,
            R_or=r_agg,
            phi_moi=phi_agg,
            gate=gate_agg,
            regime=regime,
            evidence=evidence,
            falsifier=falsifier,
            next_action=next_action,
        )
