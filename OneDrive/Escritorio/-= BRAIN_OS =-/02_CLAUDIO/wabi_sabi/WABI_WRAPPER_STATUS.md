# WABI WRAPPER STATUS — Consolidado

**Fecha consolidación:** 2026-06-16  
**Fuentes:** `ESTADO.txt` + `ESTAwqwqwqwDO.txt` (pending for review)  
**Estado canónico:** `wabi_gpt_wrapper.py` IMPLEMENTADO en `02_CLAUDIO/wabi_sabi/`

---

## RESUMEN EJECUTIVO

El wrapper Wabi-Sabi/GPT está **implementado y funcional** en `wabi_gpt_wrapper.py` (569 líneas, stdlib-only core). La formalización matemática está en `TEORIA.md`. Este documento consolida las iteraciones de análisis previas para trazabilidad histórica.

---

## ITERACIONES HISTÓRICAS (Cronológicas)

### Iteración 1 — Análisis Arquitectónico (ESTADO.txt → bloque 1)
**Hallazgo central:** Diferencia de **política de uso**, no capacidad computacional.
- GPT puede: generar 1 respuesta, 10 respuestas, hipótesis contradictorias, estimar incertidumbre, enumerar interpretaciones, mantener preguntas abiertas.
- "GPT no puede ser Wabi-Sabi" = **INFERENCIA arquitectónica**, no CERTEZA.
- **Arquitectura propuesta:** Wabi-Sabi como OS epistémico sobre GPT como CPU cognitiva.

**Wrapper mínimo propuesto:**
```python
class WabiGPT:
    def ask(self, prompt):
        raw = gpt(prompt)
        return {
            "answer": raw,
            "certainty": extract_certainties(raw),
            "inference": extract_inferences(raw),
            "unknowns": extract_unknowns(raw),
            "blocked": extract_blocked(raw),
            "residue": estimate_residue(raw)
        }
```

### Iteración 2 — Fronteras Topológicas (ESTADO.txt → bloque 2)
**CERTEZA:**
- Diferencia fundamental = topológica (manejo de imperfección)
- GPT = operador convergencia 𝒞 → R→0 (colapso térmico)
- Wabi-Sabi = operador imperfección ℐ → R→1 (expansión residuo + patina)
- Capas distintas: GPT = CPU cognitiva, Wabi-Sabi = OS epistémico

**INFERENCIA:**
- Wrapper viable: Wabi-Sabi envuelve GPT
- Interceptar salida → evitar colapso → preservar nube respuestas → mantener T=1
- Modos: `/wabi mode gpt|osit|research` con hiperparámetros diferenciados

**INCÓGNITA:** Método óptimo extracción R desde APIs cerradas (sin logits).

### Iteración 3 — Arquitectura Dual Residuo (ESTADO.txt → bloque 3)
**CERTEZA:** Cálculo R difiere en caja blanca (local) vs caja negra (API).

**INFERENCIA:** Strategy Pattern requerido:
- **Vía A (Logits/Local):** Entropía Shannon sobre distribución probabilidad token
- **Vía B (Semántica/API):** Self-Consistency + prompts auto-auditoría para varianza semántica

**INCÓGNITA:** Latencia aceptable (Vía B = múltiples llamadas API).

**Implementación:** `ResidueAnalyzer` con dual-path (engine_type: local_whitebox / api_blackbox).

### Iteración 4 — Wrapper Monolítico OSIT (ESTAwqwqwqwDO.txt → bloque 1)
**Formalización matemática completa:**
- Φ_eff(R) = exp(-νR/(J_c-R)) — ley interferencia no lineal (jamming)
- χ* ≈ 0.567 — umbral saturación epistémica
- R_or = 1 - ∏(1-r_i) — Noisy-OR combinatorio 7D
- ActionGates: BLOCK (R≥0.80), REVIEW (R≥0.567), APPROVE (R<0.567)

**Implementación:** `wabi_osit_wrapper.py` — `WabiGPTWrapper` + `ResidueAnalyzer` + `ActionGates`
- Parseo bloques OSIT determinista
- Estimación residuo vía Jaccard (caja negra)
- Temperatura dinámica (1.0 modo OSIT, 0.4 modo normal)
- Muestreo alternativo para varianza

### Iteración 5 — Integración FCU v2.0 (ESTAwqwqwqwDO.txt → bloque 2)
**Integración producción:** `WabiFCUWrapper` acoplado a FCU v2.0
- Persistencia local-first: `fcu_fingerprint.json` + `fcu_decisions.json`
- Patina materializada: I_seq = Σ λ^{n-i} · I(e_i) con decaimiento λ=0.85
- Pipeline unificado: carga fingerprint → ejecuta motor → analiza imperfección → ActionGates → persiste estado
- JammingGate TS-F6 estricto: R_or ≥ 0.80 → BLOCK irrevocable
- SHA3-256 fingerprints en handoffs

**Código:** `wabi_fcu_core.py` — `FCU20Manager` + `WabiOSITEngine` + `WabiFCUWrapper`

---

## IMPLEMENTACIÓN CANÓNICA ACTUAL: `wabi_gpt_wrapper.py`

### Arquitectura (569 líneas, stdlib-only core)

| Componente | Descripción |
|------------|-------------|
| `LLMEngine` (ABC) | Interfaz abstracta: OllamaEngine, OpenAIEngine, AnthropicEngine |
| `ResidueEstimator` | Dual-path: OSIT-tag parsing (Path A) + Jaccard variance (Path B) → Fraction exacta |
| `OSITParser` | Extrae estados CERTEZA/INFERENCIA/INCÓGNITA/BLOQUEO/ACCIÓN/ARTEFACTO/HANDOFF |
| `WabiSabiOS` | Orquestador principal: 4 modos, WitnessLog, Kintsugi, STOP gate, fingerprints |

### 4 Modos de Operación

| Modo | T | Residuo | Alternativas | Witness | OSIT Format | Kintsugi |
|------|---|---------|--------------|---------|-------------|----------|
| `gpt` | 0.7 | ❌ | ❌ | ❌ | ❌ | ❌ |
| `osit` | 1.0 | ✅ | ❌ | ✅ | ✅ | ❌ |
| `research` | 0.4 | ✅ | ✅ | ✅ | ✅ | ❌ |
| `wabi` | 1.0 | ✅ | ✅ | ✅ | ✅ | ✅ |

### Invariantes OSIT Mantenidos
1. **Aritmética exacta** — `Fraction` para R ∈ [0,1], sin floating point en core
2. **SHA3-256 fingerprints** — 12 chars en handoffs
3. **WitnessLog acumulativo** — Patina A2 (τ, κ, R history)
4. **Kintsugi paths (A4)** — Cada reparación = grieta dorada = d_eff + 1
5. **STOP gate** — R_est ≥ 0.80 → no actuar, devolver estado SATURADO

### Engines Soportados

```python
# Local (CPU-only, sin GPU)
engine = OllamaEngine(model="mistral")  # o qwen2.5-coder:3b, llama3.2:3b

# Cloud (requiere API keys en wabi.env)
engine = OpenAIEngine(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o")
engine = AnthropicEngine(api_key=os.getenv("ANTHROPIC_API_KEY"), model="claude-sonnet-4-6")

# Uso
wabi = WabiSabiOS(engine, mode="osit")
result = wabi.query("¿Puede un sistema formal conocer sus propios límites?")
# result: {answer, mode, R, R_exact, epistemic_states, alternatives, kintsugi_count, fingerprint}
```

---

## PLAN DE INTEGRACIÓN PENDIENTE

| Módulo | Qué Falta | Prioridad |
|--------|-----------|-----------|
| `core/wabi.py` | Integrar `/wabi mode gpt|osit|research|wabi` usando `WabiSabiOS` | P1 |
| `wabi_sabi/adapters/` | Conectar engines con provider registry existente (`wabi_provider_registry.py`) | P1 |
| `tests/test_wabi_gpt_wrapper.py` | Smoke Ollama, residue estimation, mode switching, fingerprints, STOP gate | P1 |
| `wabi_sabi/cli/` | TUI split-screen: sticky plan panel, `/model`, `/continue`, thinking indicator | P0 |

---

## MÉTRICAS DE VALIDACIÓN (Objetivos)

| Métrica | Target | Evidencia |
|---------|--------|-----------|
| R estimation accuracy | < 0.15 error vs ground truth | Test con prompts conocidos |
| Mode switch latency | < 100ms | Benchmark local |
| STOP gate precision | 0 false negatives (R≥0.80 never acts) | Stress test |
| Fingerprint uniqueness | 0 collisions in 10k runs | Statistical test |
| WitnessLog growth | O(1) append, no memory leak | 1000 queries test |

---

## HANDOFF

**Estado:** Wrapper core IMPLEMENTADO + Teoría CANÓNICA (TEORIA.md)  
**Siguiente:** Integración en `core/wabi.py` (modos) + CLI TUI + Tests  
**Riesgo:** Ninguno bloqueante — core es stdlib-only, compatible con arquitectura existente  
**Decisiones:** Strategy Pattern para ResidueEstimator confirmado; Fraction para aritmética exacta confirmado; 4 modos operacionales confirmados