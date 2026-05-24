# Agent Channels

## Canales minimos

| Canal | Proposito | Visibilidad | Retencion |
|---|---|---|---|
| `#system_announcements` | Boletines generales y decisiones de sistema | system | project |
| `#handoffs` | Transferencias con fingerprint y evidencia | team | permanent |
| `#witnesslog` | Eventos append-only y hash-chain | system | permanent |
| `#tasks` | Cola de trabajo y cierres verificables | team | project |
| `#security_review` | Secretos, privacidad, ZIPs, publicacion | system | permanent |
| `#canon_updates` | Cambios de canon y frontera epistemica | team | permanent |
| `#build_reports` | Build, test, validacion y artifact registry | team | project |
| `#research` | Comparaciones y material investigativo public-safe | team | project |
| `#lovable_ui` | Ruta React/Lovable y HUD local | team | project |
| `#codex_runs` | Corridas Codex, fingerprints y handoffs | team | permanent |
| `#claudio_local` | Claudio local y COMMS privado | private | project |
| `#wabi_sabi_orchestration` | Orquestacion local y politicas Wabi-Sabi | private | project |
| `#duat_product` | Producto, UX, roadmap local | team | project |

## Agentes minimos

| Agente | Rol | Estado seed |
|---|---|---|
| `wabi_sabi_orchestrator` | Coordina rutas locales y evita expansion sin cierre | working |
| `cerebro_canon` | Custodia canon y fronteras epistemicas | reviewing |
| `claudio_local_operator` | Opera superficies Claudio locales | idle |
| `codex_engineer` | Implementa, prueba y documenta | working |
| `lovable_frontend` | Mantiene UI React/Lovable | working |
| `security_gate` | Bloquea secretos, deploy y publicacion | blocked |
| `research_scout` | Compara frameworks y traduce patrones | reviewing |
| `duat_product_designer` | Define producto y UX operacional | idle |
| `lore_archivist` | Protege material editorial/privado | idle |
| `human_operator` | Gate humano final | idle |

## Seed implementado

La semilla mock de estos canales/agentes esta en:

`C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\messagebus\seed.ts`

El siguiente paso es mover el seed canonico a JSONL/SQLite local y hacer que la UI lo consuma como adaptador, no como duplicado manual.
