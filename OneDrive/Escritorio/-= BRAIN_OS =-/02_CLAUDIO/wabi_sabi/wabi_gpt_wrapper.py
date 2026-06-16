"""
WabiSabi-GPT Wrapper — OSIT Framework v3.7
==========================================
OS epistémico (Wabi-Sabi) sobre cualquier LLM engine (GPT/Claude/Ollama).

Topología:
  GPT:   𝒞(E) = softmax(l/T)      → R → 0  (colapso térmico)
  Wabi:  ℐ(E) = E + α·R(E)·G(E)   → R → 1  (expansión de residuo)

Arquitectura:
  Usuario → WabiSabiOS → LLMEngine (CPU cognitiva) → WabiSabiOS → Output OSIT

Principios:
  - Aritmética exacta (Fraction) para R ∈ [0,1] — sin floating point en capa core
  - SHA3-256 fingerprints en handoffs
  - Stdlib-only para núcleo; imports de API opcionales
  - CPU-only compatible (Ollama local)

Autor: Luis René González López / Lutren — OSIT v3.7
"""

import re
import json
import hashlib
from abc import ABC, abstractmethod
from fractions import Fraction
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTES OSIT
# ═══════════════════════════════════════════════════════════════════════════════

OSIT_SYSTEM_PROMPT = """Eres un nodo epistémico OSIT. Responde SIEMPRE con esta estructura:

ESTADO
R estimado: [0.0-1.0] | Régimen: [ÓPTIMO/FUNCIONAL/CARGADO/SATURADO]

CERTEZA
[afirmaciones respaldadas por evidencia o lógica]

INFERENCIA
[afirmaciones plausibles, no demostradas]

INCÓGNITA
[puntos sin información suficiente]

ACCIÓN
[próximo paso lógico]

ARTEFACTO
[resultado concreto, código, o texto]

HANDOFF
Fingerprint: [hash corto]
Brief: [resumen en 1-2 líneas]"""

# Pesos epistémicos para cálculo de R via tags OSIT
# R=0 → certeza absoluta, R=1 → incertidumbre máxima
EPISTEMIC_WEIGHTS: dict[str, Fraction] = {
    "CERTEZA":    Fraction(0),
    "INFERENCIA": Fraction(1, 2),
    "INCÓGNITA":  Fraction(1),
    "INCOGNITA":  Fraction(1),
    "BLOQUEO":    Fraction(9, 10),  # No llega a 1: bloqueo ≠ incertidumbre total
}

MODE_CONFIGS: dict[str, dict] = {
    # GPT puro: fluidez, sin rastreo epistémico
    "gpt": {
        "T": 0.7,
        "residue": False,
        "alternatives": False,
        "witness": False,
        "osit_format": False,
    },
    # OSIT estándar: trazabilidad + residuo
    "osit": {
        "T": 1.0,
        "residue": True,
        "alternatives": False,
        "witness": True,
        "osit_format": True,
    },
    # Research: baja temperatura + búsqueda de alternativas
    "research": {
        "T": 0.4,
        "residue": True,
        "alternatives": True,
        "witness": True,
        "osit_format": True,
    },
    # Wabi: máxima expansión de incertidumbre + kintsugi paths
    "wabi": {
        "T": 1.0,
        "residue": True,
        "alternatives": True,
        "witness": True,
        "osit_format": True,
        "kintsugi": True,
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# ENGINE ABSTRACTION — GPT/Claude/Ollama como CPU cognitiva intercambiable
# ═══════════════════════════════════════════════════════════════════════════════

class LLMEngine(ABC):
    """Interfaz abstracta: cualquier LLM actúa como motor bajo WabiSabi OS."""

    @abstractmethod
    def generate(self, prompt: str, system: str = "", temperature: float = 1.0) -> str:
        """Genera una respuesta."""

    @abstractmethod
    def generate_n(self, prompt: str, n: int, temperature: float = 1.0) -> list[str]:
        """Genera N respuestas independientes (para estimación de varianza)."""


class OllamaEngine(LLMEngine):
    """
    Motor Ollama — CPU-only, sin GPU requerida.
    Acceso a logprobs disponible si el modelo los expone.
    """

    def __init__(self, model: str = "mistral", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def _call(self, prompt: str, system: str = "", temperature: float = 1.0) -> dict:
        import urllib.request
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system,
            "stream": False,
            "options": {"temperature": temperature},
        }
        req = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())

    def generate(self, prompt: str, system: str = "", temperature: float = 1.0) -> str:
        return self._call(prompt, system, temperature).get("response", "")

    def generate_n(self, prompt: str, n: int = 3, temperature: float = 1.0) -> list[str]:
        return [self.generate(prompt, temperature=temperature) for _ in range(n)]


class OpenAIEngine(LLMEngine):
    """Motor OpenAI (GPT-4o, GPT-4, etc.) — sin acceso a logits internos."""

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, system: str = "", temperature: float = 1.0) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=min(temperature, 2.0),
        )
        return response.choices[0].message.content

    def generate_n(self, prompt: str, n: int = 3, temperature: float = 1.0) -> list[str]:
        return [self.generate(prompt, temperature=temperature) for _ in range(n)]


class AnthropicEngine(LLMEngine):
    """Motor Anthropic Claude — temperatura máxima 1.0."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        import anthropic
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, system: str = "", temperature: float = 1.0) -> str:
        kwargs: dict = {
            "model": self.model,
            "max_tokens": 2048,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": min(temperature, 1.0),  # Anthropic cap = 1.0
        }
        if system:
            kwargs["system"] = system
        response = self.client.messages.create(**kwargs)
        return response.content[0].text

    def generate_n(self, prompt: str, n: int = 3, temperature: float = 1.0) -> list[str]:
        return [self.generate(prompt, temperature=temperature) for _ in range(n)]


# ═══════════════════════════════════════════════════════════════════════════════
# RESIDUE ESTIMATOR — R ∈ [0,1] via Fraction (exacta)
# ═══════════════════════════════════════════════════════════════════════════════

class ResidueEstimator:
    """
    Estimación de R ∈ [0,1] sin acceso a logits internos.

    Dual-path:
      A) OSIT-parse:  cuenta claims por tag (CERTEZA=0, INFERENCIA=0.5, INCÓGNITA=1)
      B) Varianza:    distancia Jaccard entre N muestras independientes

    Path A es el principal. Path B se activa cuando hay muestras disponibles
    (modos research/wabi) y se combina con A como media armónica.
    """

    def from_osit_tags(self, text: str) -> Fraction:
        """
        Path A: parsea secciones OSIT y pondera claims por peso epistémico.
        Retorna R=0.5 si no hay tags (máxima incertidumbre sin evidencia).
        """
        state_pattern = "|".join(EPISTEMIC_WEIGHTS.keys())
        section_regex = re.compile(
            rf"(?:^|\n)\*?({state_pattern})\*?\s*[:\n](.*?)(?=\n\*?(?:{state_pattern})\*?[:\n]|\Z)",
            re.DOTALL | re.IGNORECASE,
        )

        total_weight = Fraction(0)
        total_claims = 0

        for match in section_regex.finditer(text):
            tag = match.group(1).upper()
            content = match.group(2).strip()
            weight = EPISTEMIC_WEIGHTS.get(tag, Fraction(1, 2))

            # Cuenta líneas no vacías como claims individuales
            claims = [l.strip().lstrip("*-•1234567890.").strip()
                      for l in content.split("\n") if l.strip().lstrip("*-•1234567890.").strip()]
            n = len(claims) or 1

            total_weight += weight * n
            total_claims += n

        if total_claims == 0:
            return Fraction(1, 2)

        return total_weight / total_claims

    def from_variance(self, samples: list[str]) -> Fraction:
        """
        Path B: distancia Jaccard promedio entre pares de muestras.
        Alta varianza → respuestas inestables → R alto.
        """
        if len(samples) < 2:
            return Fraction(1, 2)

        def tokenize(t: str) -> frozenset:
            return frozenset(re.findall(r"\b\w+\b", t.lower()))

        sets = [tokenize(s) for s in samples]
        n = len(sets)
        total_dist = Fraction(0)
        pairs = 0

        for i in range(n):
            for j in range(i + 1, n):
                inter = len(sets[i] & sets[j])
                union = len(sets[i] | sets[j])
                if union > 0:
                    total_dist += Fraction(union - inter, union)  # Jaccard distance exacta
                    pairs += 1

        return total_dist / pairs if pairs else Fraction(1, 2)

    def combined(self, text: str, samples: Optional[list[str]] = None) -> Fraction:
        """
        Combinación: si hay muestras, media armónica de ambos paths.
        Sin muestras: solo Path A.
        """
        r_a = self.from_osit_tags(text)
        if not samples or len(samples) < 2:
            return r_a
        r_b = self.from_variance(samples)
        # Media armónica: penaliza si alguno es 0
        if r_a == 0 and r_b == 0:
            return Fraction(0)
        return Fraction(2) * r_a * r_b / (r_a + r_b)


# ═══════════════════════════════════════════════════════════════════════════════
# OSIT PARSER — extrae estados epistémicos del output del LLM
# ═══════════════════════════════════════════════════════════════════════════════

class OSITParser:
    """Segmenta respuesta LLM en estados OSIT."""

    ALL_STATES = [
        "ESTADO", "CERTEZA", "INFERENCIA", "INCÓGNITA", "INCOGNITA",
        "BLOQUEO", "ACCIÓN", "ACCION", "ARTEFACTO", "HANDOFF",
    ]

    def extract(self, text: str) -> dict:
        pattern = "|".join(self.ALL_STATES)
        section_regex = re.compile(
            rf"(?:^|\n)\*?({pattern})\*?\s*[:\n](.*?)(?=\n\*?(?:{pattern})\*?[:\n]|\Z)",
            re.DOTALL | re.IGNORECASE,
        )

        result: dict = {
            "CERTEZA": [],
            "INFERENCIA": [],
            "INCÓGNITA": [],
            "BLOQUEO": [],
            "ACCIÓN": "",
            "ARTEFACTO": "",
            "HANDOFF": "",
            "ESTADO": "",
        }

        for match in section_regex.finditer(text):
            tag = match.group(1).upper()
            content = match.group(2).strip()

            # Normalizar variantes
            tag = tag.replace("INCOGNITA", "INCÓGNITA").replace("ACCION", "ACCIÓN")

            if tag in ("ARTEFACTO", "HANDOFF", "ESTADO", "ACCIÓN"):
                result[tag] = content
            elif tag in result and isinstance(result[tag], list):
                items = [
                    l.strip().lstrip("*-•1234567890.").strip()
                    for l in content.split("\n")
                    if l.strip().lstrip("*-•1234567890.").strip()
                ]
                result[tag] = items

        return result


# ═══════════════════════════════════════════════════════════════════════════════
# WABI-SABI OS — capa de orquestación epistémica
# ═══════════════════════════════════════════════════════════════════════════════

class WabiSabiOS:
    """
    Sistema operativo epistémico OSIT.
    El LLM subyacente (GPT/Claude/Ollama) opera como CPU cognitiva intercambiable.

    Modos de operación:
      /wabi mode gpt       → fluidez pura, sin rastreo epistémico
      /wabi mode osit      → trazabilidad OSIT, residuo, WitnessLog
      /wabi mode research  → multi-muestra + alternativas ortogonales
      /wabi mode wabi      → máxima expansión de incertidumbre (kintsugi paths)

    Invariantes OSIT mantenidos:
      - Aritmética exacta (Fraction) para R
      - SHA3-256 en fingerprints de handoff
      - WitnessLog acumulativo (patina: A2)
      - R_est ≥ 0.80 → STOP (no actuar sin suficiente señal)
    """

    R_STOP_THRESHOLD = Fraction(4, 5)  # 0.80 — no actuar si R supera esto

    def __init__(self, engine: LLMEngine, mode: str = "osit"):
        assert mode in MODE_CONFIGS, f"Modo inválido: {mode}"
        self.engine = engine
        self.mode = mode
        self.witness_log: list[dict] = []
        self._estimator = ResidueEstimator()
        self._parser = OSITParser()
        self._kintsugi_count = 0  # A4: cuenta reparaciones (dimensión)

    # ── INTERFACE ─────────────────────────────────────────────────────────────

    def set_mode(self, mode: str) -> None:
        """Cambia modo en caliente — sin reiniciar WitnessLog."""
        assert mode in MODE_CONFIGS, f"Modo inválido. Opciones: {list(MODE_CONFIGS)}"
        self.mode = mode

    def query(self, prompt: str) -> dict:
        """
        Pipeline principal.
        Retorna dict con estructura OSIT + metadatos de residuo.
        """
        cfg = MODE_CONFIGS[self.mode]
        system = OSIT_SYSTEM_PROMPT if cfg["osit_format"] else ""

        # ── GENERACIÓN ──────────────────────────────────────────────────────
        if cfg.get("kintsugi"):
            # Modo wabi: 3 muestras para varianza + preserva todas como grietas
            samples = self.engine.generate_n(prompt, n=3, temperature=cfg["T"])
            raw = samples[0]
            self._kintsugi_count += 1
        elif cfg.get("alternatives"):
            # Modo research: muestras para varianza, no como grietas
            samples = self.engine.generate_n(prompt, n=3, temperature=cfg["T"])
            raw = samples[0]
        else:
            raw = self.engine.generate(prompt, system=system, temperature=cfg["T"])
            samples = None

        # ── MODO GPT PURO: retorno mínimo ────────────────────────────────────
        if not cfg["residue"]:
            return {"answer": raw, "mode": "gpt", "residue": None}

        # ── PIPELINE EPISTÉMICO ──────────────────────────────────────────────
        R = self._estimator.combined(raw, samples)

        # Invariante: R ≥ 0.80 → STOP
        if R >= self.R_STOP_THRESHOLD:
            return self._stop_response(prompt, raw, R)

        osit_states = self._parser.extract(raw) if cfg["osit_format"] else {}

        alternatives = []
        if cfg.get("alternatives"):
            alternatives = self._kintsugi_paths(prompt, cfg)

        fingerprint = self._fingerprint(raw)

        result = {
            "answer":           raw,
            "mode":             self.mode,
            "R":                float(R),
            "R_exact":          str(R),           # Fracción exacta
            "epistemic_states": osit_states,
            "alternatives":     alternatives,
            "kintsugi_count":   self._kintsugi_count,
            "fingerprint":      fingerprint,
        }

        if cfg["witness"]:
            self._log(prompt, result)

        return result

    # ── KINTSUGI PATHS (A4: cada grieta aumenta d_eff) ───────────────────────

    def _kintsugi_paths(self, prompt: str, cfg: dict) -> list[str]:
        """
        Genera 3 interpretaciones ortogonales (grietas doradas).
        Cada path es una dirección de máxima incertidumbre, no una variante.
        """
        alt_system = (
            "Genera exactamente 3 interpretaciones RADICALMENTE distintas de la pregunta. "
            "No variantes de la misma idea. Cada interpretación en ≤3 líneas. "
            "Separadas por '---'. Sin numeración."
        )
        raw_alts = self.engine.generate(prompt, system=alt_system, temperature=cfg["T"])
        return [p.strip() for p in raw_alts.split("---") if p.strip()]

    # ── WITNESS LOG (A2: patina acumulativa) ─────────────────────────────────

    def _log(self, query: str, result: dict) -> None:
        entry = {
            "step":       len(self.witness_log),
            "mode":       self.mode,
            "q_hash":     self._fingerprint(query),
            "R":          result["R"],
            "alts":       len(result.get("alternatives", [])),
            "kintsugi":   self._kintsugi_count,
            "fp":         result["fingerprint"],
        }
        self.witness_log.append(entry)

    # ── STOP RESPONSE (R ≥ 0.80) ─────────────────────────────────────────────

    def _stop_response(self, prompt: str, raw: str, R: Fraction) -> dict:
        """
        Invariante OSIT: R_est ≥ 0.80 → STOP.
        No actuar; devolver estado de alta saturación.
        """
        return {
            "answer":      raw,
            "mode":        self.mode,
            "R":           float(R),
            "R_exact":     str(R),
            "STOP":        True,
            "regime":      "SATURADO",
            "reason":      f"R={float(R):.3f} ≥ 0.80 — incertidumbre demasiado alta para acción",
            "fingerprint": self._fingerprint(raw),
        }

    # ── FINGERPRINT (SHA3-256, 12 chars) ─────────────────────────────────────

    @staticmethod
    def _fingerprint(text: str) -> str:
        return hashlib.sha3_256(text.encode()).hexdigest()[:12]

    # ── ACCESSORS ─────────────────────────────────────────────────────────────

    def get_witness_log(self) -> list[dict]:
        return self.witness_log

    def current_R(self) -> Optional[float]:
        """R del último query (desde WitnessLog)."""
        return self.witness_log[-1]["R"] if self.witness_log else None

    def reset(self) -> None:
        """Limpia WitnessLog y contador kintsugi. Mantiene engine y modo."""
        self.witness_log.clear()
        self._kintsugi_count = 0


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO — CPU-only con Ollama (sin GPU)
# ═══════════════════════════════════════════════════════════════════════════════

def demo_ollama():
    """
    Demo básico con Ollama local.
    Requiere: ollama pull mistral  (o cualquier modelo compatible)
    Hardware: funciona en Dell i5 / Iris Xe / 8GB RAM
    """
    engine = OllamaEngine(model="mistral")
    wabi = WabiSabiOS(engine, mode="osit")

    query = "¿Puede un sistema formal conocer sus propios límites?"

    print(f"\n{'═'*60}")
    print(f"MODO: {wabi.mode.upper()} | QUERY: {query}")
    print('═' * 60)

    result = wabi.query(query)

    print(f"\nR = {result['R']:.4f}  ({result['R_exact']})")
    print(f"FINGERPRINT: {result['fingerprint']}")

    if result.get("STOP"):
        print(f"\n[STOP] {result['reason']}")
        return

    print(f"\nRESPUESTA:\n{result['answer'][:500]}...")

    if result["epistemic_states"].get("CERTEZA"):
        print(f"\nCERTEZA: {result['epistemic_states']['CERTEZA']}")
    if result["epistemic_states"].get("INCÓGNITA"):
        print(f"INCÓGNITA: {result['epistemic_states']['INCÓGNITA']}")

    # Cambiar a modo wabi para comparar expansión de residuo
    wabi.set_mode("wabi")
    result_w = wabi.query(query)

    print(f"\n{'─'*60}")
    print(f"MODO WABI — R = {result_w['R']:.4f}")
    print(f"Kintsugi paths: {len(result_w['alternatives'])}")
    print(f"WitnessLog entries: {len(wabi.get_witness_log())}")
    print(f"d_eff aumentó: {wabi._kintsugi_count} reparaciones")


def demo_api(anthropic_key: str):
    """
    Demo con Anthropic API.
    Residuo estimado via OSIT tag parsing (sin logits).
    """
    engine = AnthropicEngine(api_key=anthropic_key)
    wabi = WabiSabiOS(engine, mode="research")

    result = wabi.query("¿Qué distingue conocimiento de creencia justificada?")

    print(f"R = {result['R']:.4f}  |  Alternativas: {len(result['alternatives'])}")
    print(f"Fingerprint: {result['fingerprint']}")
    return result


if __name__ == "__main__":
    demo_ollama()