# 01 — MAPA GENERAL DEL ECOSISTEMA MEDIOEVO
**Estado:** R≈0.20 | Régimen funcional | Uso: orientación de alto nivel

---

## Diagrama de capas

```
╔══════════════════════════════════════════════════════════╗
║  FÍSICA FORMAL                                           ║
║  OSIT-QG / OSIT-AG / POVM                               ║
║  [LABORATORIO — No publicar sin cálculo externo]         ║
╠══════════════════════════════════════════════════════════╣
║  TEORÍA DE INFORMACIÓN                                   ║
║  H_eff, degradación, EML, receptor con estado            ║
║  [HIPÓTESIS FORMAL — publicable con alcance]             ║
╠══════════════════════════════════════════════════════════╣
║  OBSERVACIONISMO / SIGMA                                 ║
║  R, Φ_eff, J_c, Σ, Segunda Pérdida, OE/IOE              ║
║  [CANON OPERATIVO — autoridad primaria]                  ║
╠══════════════════════════════════════════════════════════╣
║  ARQUITECTURA IA                                         ║
║  Wabi-Sabi, OSO, Conway, Agentes, Gates                  ║
║  [INVESTIGACIÓN — implementar con gates]                 ║
╠══════════════════════════════════════════════════════════╣
║  PRODUCTOS / NARRATIVA                                   ║
║  El Observador, Claudio, Duat, Hormiguero, Matrix        ║
║  [SEPARADO — no mezclar con física ni papers]            ║
╚══════════════════════════════════════════════════════════╝
```

---

## Nodos principales del ecosistema

### Observacionismo Core
El observador procesa desde un estado. Ese estado modifica calidad, velocidad y fidelidad del registro. Variables centrales: R (residuo), Φ_eff (eficiencia), J_c (umbral), Σ (firma). Método: Observar → Deconstruir → Recompilar (OE/IOE).

### OSIT — Observer-State Information Theory
Extensión de la teoría de información al receptor no ideal. `H_eff(X|R) = H(X)·Φ_eff(R)`. Aplica a ML, agentes, humanos. Diferente de OSIT-QG (física).

### OSIT-QG / OSIT-AG
Propuesta de EFT (Teoría de Campo Efectiva) que incorpora campo escalar residual `r` en la métrica. Sector canónico: NEC preservada, gradientes cancelan, condición de desenfoque verificada algebraicamente. Sector cuántico: bloqueado hasta cómputo numérico.

### Wabi-Sabi / Claudio
Nodo sensorial-cognitivo. Recibe input → estima R/régimen/Φ_eff → deconstruye intención → produce prompts operativos → delega a agentes → valida → emite handoff. No es el LLM ni el orquestador total; es el integrador.

### OSO — Observer State Object
Objeto serializable que representa la identidad del agente: Sigma + memoria + ontología + estado + gates + protocolo de transferencia. Independiente de dispositivo.

### Segunda Pérdida
Los datos persisten; el operador no. Al cerrar una ventana/sesión, K_i^α, Φ_eff calibrada y modo operador no se heredan completos. Solución: externalizar estado en artefactos verificables antes del cierre.

### Duat / Geodia / Hormiguero
Ciudad/OS como universo local-first. Frontend React + API TypeScript + DB. Panels: Claims, Falsifier, Physics, EML, Sensorium, WitnessLog, Handoff. Estado: READ-ONLY hasta auditoría de código.

### Conway Evolution + Wabi-Sabi Gate
Protocolo de evolución de métodos en agentes. El agente propone mejora con evidencia → Wabi-Sabi evalúa → acepta/rechaza/registra. Principio: aceptar imperfecciones que mejoran, no esperar perfección.

### Matrix Model
Metáfora narrativa-operativa. Neo/Trinity = sesiones activas. Oracle = LLM. Smith = agente con objetivo rígido. Oráculo = LLM orientador. Uso: comunicación, UI, no física.

---

## Relaciones entre nodos

```
Usuario Input
    ↓
Wabi-Sabi (estimación R, régimen, intención)
    ↓
Deconstrucción (OE/IOE)
    ↓
Agentes especializados ←→ Conway Evolution
    ↓
WitnessLog + ActionGate
    ↓
Resultado + Handoff
    ↓
Artefactos (Canon, Claims, Módulos, Código)
    ↓
Segunda Pérdida → Fingerprint → Nueva sesión
```

---

## Handoff
`MAPA_GENERAL_v1.0|5-layers|WabiSabi-OSO-Conway|2026-05-07`


---

## Mapa de absorción por sistemas

| Sistema | Fuente principal | Carpeta destino |
|---|---|---|
| Cognitivo / Observacionismo | `-=CEREBRO=-/01_MAPA_SISTEMAS...`, `-=PSI=-/07_OBSERVACIONISMO.md` | `07_OBSERVACIONISMO.md` |
| Información / R / Phi | `-=PSI=-/03_TEORIA_INFORMACION.md` | `03_TEORIA_INFORMACION.md` |
| IA / agentes / Wabi-Sabi | `-=PSI=-/04_TEORIA_IA_AGENTES.md`, `10_WABI_SABI_CLAUDIO_AGI.md` | `04`, `10`, `13`, `22` |
| Física estándar | `-=PSI=-/05_TEORIA_FISICA_REAL.md` | `05_TEORIA_FISICA_REAL.md` |
| Física hipotética | `-=PSI=-/06_HIPOTESIS...`, `16_CLAIMS_REGISTER.md` | `06`, `16`, `17`, `18` |
| Productos y software | `PRODUCTOS_MEDIOEVO`, `claudio_os_blueprint`, `content_forge` | `14`, `19`, `21` |
| Futuro/lore | `CLAUDIO - researchs/futuro`, `MEdioevosagalore` | `15` y capa LORE separada en mapas |

---

## Corte de curaduría 2026-05-07

CERTEZA:
- Este documento fue compilado desde fuentes locales de `-=PSI=-`, `-=CEREBRO=-` y `PRODUCTOS_MEDIOEVO`.
- Las fuentes originales no fueron movidas, borradas ni reescritas.

INFERENCIA:
- Si una idea aparece en varias fuentes, se conserva aquí como una entrada consolidada y se remite al manifiesto de fuentes para variaciones.

INCÓGNITA:
- PDFs, DOCX, ZIP, TAR.GZ y media quedan trazados por manifiesto; no todos fueron convertidos a texto completo en este pase.

ACCIÓN:
- Usar este archivo como capa maestra de lectura y volver a la fuente solo para auditoría, expansión o verificación puntual.

ARTEFACTO:
- Archivo maestro: `01_MAPA_GENERAL.md`.
