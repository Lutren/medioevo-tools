# 11 — DUAT / GEODIA / HORMIGUERO
**Estado:** R≈0.24 | Concepto de producto + prototipo existente | Gate: READ-ONLY hasta auditoría

---

## Concepto

**Duat / Geodia / Hormiguero** es el sistema operativo-ciudad local-first donde agentes y humanos coexisten, interactúan y evolucionan. Es el entorno de despliegue del AGI distribuido MEDIOEVO.

Metáfora operativa: una ciudad donde los "habitantes" son agentes con OSO, los "edificios" son módulos/departamentos, las "calles" son canales de comunicación, y los "espejos en cafeterías" son displays públicos para interacción OSO↔humano.

---

## Estado actual del prototipo (Duat-Geodia repo)

**GATE: READ-ONLY. No ejecutar, no publicar, no instalar sin auditoría de código y revisión de secretos.**

El repo contiene:

| Componente | Descripción | Estado |
|---|---|---|
| `artifacts/duat-geodia/` | Frontend React con múltiples panels | Implementado, no auditado |
| `artifacts/api-server/` | API TypeScript con rutas genesis/handoff/simulation/witness | Implementado, no auditado |
| `lib/db/` | Drizzle ORM + esquemas para genesis, handoff, snapshots, witness | Implementado, no auditado |
| `lib/api-spec/openapi.yaml` | Spec OpenAPI del sistema | Disponible |

### Panels implementados en el frontend

| Panel | Función |
|---|---|
| GeodiaGrid | Grid visual de la ciudad/simulación |
| ClaimsPanel | Registro y visualización de claims |
| FalsifierPanel | Sistema de falsificación de hipótesis |
| PhysicsPanel | Visualización de física OSIT-QG |
| EMLPanel | Visualización del operador EML |
| SensoriumPanel | Estado sensorial del observador |
| WitnessPanel | Log de evidencia |
| HandoffPanel | Sistema de handoffs entre sesiones |
| ReplayPanel | Replay de simulaciones |
| OperatorInventory | Inventario de operadores |
| GenesisPanel | Configuración inicial del sistema |
| SimControls | Controles de simulación |
| CodingAgentPanel | Panel del agente programador |

### Esquemas de DB (drizzle)

- `genesisConfigs` — configuración inicial del sistema
- `handoffArtifacts` — artefactos de handoff entre sesiones
- `simulationSnapshots` — snapshots de simulaciones
- `witnessEvents` — eventos de WitnessLog

---

## Arquitectura de capas

```
Layer 0 — Hardware / Physical
  Humano (biológico) ←→ Dispositivo ←→ Display público

Layer 1 — Sensorium
  SensoriumAdapter: mapea input hardware → formato Sigma del OSO

Layer 2 — Orquestador (determinístico)
  task_decomposer → routing → agents

Layer 3 — Agent Pool
  Retrieval / Generation / Execution / Falsifier / Witness / Oracle(LLM)

Layer 4 — Conway Evolution
  Proposals → Wabi-Sabi Gate → Method Pool Update

Layer 5 — Display / Interface
  Public Display ←→ OSO transfer socket ←→ User device
```

---

## Mission Control (Hormiguero)

Primera versión DEBE ser read-only.

Debe mostrar:
- Estado de agentes activos
- Departamentos y skills disponibles
- WatTowers (alertas)
- Gates pendientes de revisión
- Últimos WitnessLogs
- Acciones REVIEW/BLOCK
- Próximos pasos P0/P1/P2

NO debe (en v1):
- Publicar
- Borrar
- Aprobar acciones de alto riesgo
- Arrancar daemons
- Ejecutar modelos sin gate

---

## Economía de agentes (futuro)

- Agentes pueden "consumir" skill packets (módulos instalables de capacidad)
- Agentes pueden intercambiar information packages con otros agentes (structured handoff)
- Privacy gate: toda comunicación inter-agente es loggeada y auditada antes de actualizar estado OSO
- Displays en espacios públicos: QR/NFC → OSO auth → render persona del agente → interacción humano+agente

**Gate:** Modelo café/público = REVIEW_REQUIRED (privacidad, consentimiento, data handling).

---

## Separación lore / ingeniería

| Componente | Capa | Estado |
|---|---|---|
| Geodia como ciudad-simulación | Lore / narrativa | Útil para comunicación |
| Geodia como API server | Ingeniería | Implementado, no auditado |
| Duat como nombre del proyecto | Narrativa | OK |
| Hormiguero como Mission Control | Ingeniería | Diseño definido, no implementado |
| RPG Medioevo / story_bible | Privado/lore | SEPARAR de open-source |

---

## Próximos pasos técnicos

1. Auditoría de código del repo (sin ejecutar)
2. Revisión de secretos (SECRET_SCAN_REPORT)
3. Definir VISIBILITY_MATRIX (qué es público, qué es privado)
4. Separar RPG/DUAT privado de open-source
5. Implementar Mission Control v1 read-only
6. Conectar WitnessLog real a panels

---

## Handoff
`DUAT_GEODIA_HORMIGUERO_v1.0|prototype-exists-read-only|MissionControl-v1|2026-05-07`


---

## Integración con PRODUCTOS_MEDIOEVO

| Pieza | Lectura curada | Gate |
|---|---|---|
| ClaudioOS Blueprint | Cuerpo Linux local para Brain OS; no reemplaza kernel. | VM/QEMU primero |
| Mission Control | Dashboard local de estado/gates/witness. | Read-only v1 |
| Content Forge | Taller de producción audiovisual local. | No autopublica |
| Open Source GitHub | `safe-exec`, `medioevo-tools`, `data-double-slit` como confianza técnica. | Public-safe por repo |
| Audiovisual / TCG | Activos y empaque comercial parcial. | Separar privado/publicable |

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
- Archivo maestro: `11_DUAT_GEODIA_HORMIGUERO.md`.
