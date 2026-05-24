# MERCURY_AGENT_SOURCE_CARD_2026-05-15

## Fuente

- Repositorio: `https://github.com/cosmicstack-labs/mercury-agent`
- Sitio: `https://mercury.cosmicstack.org`
- Snapshot consultado: 2026-05-15
- Estado GitHub observado via API: `MIT`, `main`, `pushed_at=2026-05-10T16:32:16Z`, `stars=2197`, `forks=228`
- Version declarada en README/package: `v1.1.6`
- Clasificacion local: `EXTERNAL_OPEN_SOURCE_REFERENCE_REVIEW`
- ActionGate: `REVIEW` para instalar, copiar codigo, adoptar dependencias, habilitar Telegram/GitHub/Spotify o publicar una derivacion.

## Lectura corta

Mercury se parece al carril Claudio/BRAIN_OS en la ambicion de ser un agente local persistente, con identidad editable, memoria, permisos, herramientas, canales, scheduler y subagentes. La diferencia principal es de escala y presentacion: Mercury empaqueta una superficie publica compacta y consumible; MEDIOEVO/CLAUDIO contiene un sistema mas amplio con canon, gobierno de seguridad, productos comerciales, capas privadas y evidencia/handoff.

La utilidad no esta en importar Mercury entero. La utilidad esta en extraer patrones de producto y runtime que pueden endurecer una version publica-segura de Claudio sin exponer Observacionismo profundo, DUAT privado, libros completos, RPG/TCG ni secretos.

## Coincidencias directas con MEDIOEVO / CLAUDIO

| Mercury | Equivalente local | Lectura |
|---|---|---|
| Permission-hardened tools, folder scopes, approvals | `ActionGate`, `APPROVE/REVIEW/BLOCK`, `ObservationEnvelope`, host gate | Coincidencia fuerte. Mercury tiene UX simple; Claudio tiene semantica mas rica. |
| Second Brain con SQLite/FTS5, tipos de memoria y consolidacion | BRAIN_OS, COMMS, memory vault, `NEXT_SESSION_BRIEF`, fingerprints | Coincidencia fuerte. Mercury resuelve memoria como producto; Claudio prioriza evidencia y frontera. |
| Soul/persona/taste/heartbeat en Markdown | canon, agentes, prompts, perfiles, `AGENTS.md`, `CLAUDE.md` | Coincidencia fuerte. Mercury lo nombra mejor para usuario final. |
| Token budget, auto-concise | `R`, `Phi_eff`, `J_c`, jamming, contexto externo | Coincidencia conceptual. Claudio puede superar esto si convierte R/Phi en controles visibles. |
| Daemon 24/7, watchdog, scheduler | Claudio/Argus persistente, OPPO/PC1, bulletin board, pending review | Util para continuidad local y movil. |
| CLI + Telegram | CLI/API/Argus/OPPO | Mercury ya resolvio el canal humano remoto simple. |
| Skills `SKILL.md` con progressive disclosure | Codex skills, OSIT skill registry, agent packets | Coincidencia muy aprovechable para una capa interoperable. |
| Sub-agents, file locks, task board, resource manager | COMMS, agentes BRAIN_OS, workpacks, handoffs | Util, pero Claudio debe mantener `ObservationEnvelope` y bloqueo de escritura. |
| `doctor`, status, permissions, budget commands | provider status, pending review, host_observacionista, ActionGate CLI | Patron de UX muy aprovechable. |

## Que nos sirve

1. Crear un `claudio doctor` humano: diagnostico de permisos, proveedores, host gate, memoria, rutas privadas, secretos presentes/ausentes y estado de COMMS sin imprimir secretos.
2. Convertir `ActionGate` en UX de permisos: no solo dictamen tecnico, sino prompts claros tipo `Ask Me`, scopes por carpeta y manifiesto persistente.
3. Hacer una memoria publica-segura tipo `Second Brain Lite`: SQLite/FTS o JSONL indexado con tipos `decision`, `constraint`, `goal`, `project`, `episode`, pero con redaccion y boundary check antes de persistir.
4. Adoptar progressive disclosure para agentes: cargar al inicio solo nombre/descripcion/propietario/gates; cargar instrucciones completas solo cuando el agente se invoca.
5. Empaquetar una superficie publica pequena: `npx`/CLI o `pipx` equivalente, README directo, comandos concretos, docs de instalacion y demo sintetica.
6. Reusar el patron daemon sin admin: servicio de usuario, PID/log, watchdog, `status/start/stop/restart/logs`, especialmente para Argus/OPPO/PC1.
7. Crear scheduler seguro: tareas recurrentes pasan por `ActionGate`, registran evidencia y nunca publican/empujan/envian sin gate.
8. Implementar task board con locks: estados persistentes para subagentes, locks de escritura por archivo y comandos `/halt` / `/stop`.
9. Mejorar copy publico: "local-first agent runtime with permission gates, memory, skills and handoff" en vez de exponer Observacionismo propietario.
10. Mantener ADRs compactos: `DECISIONS.md` de Mercury es buen patron para explicar decisiones sin cargar el canon entero.

## Que no conviene copiar

- No usar `Allow All` como modo amplio en este workspace. Aqui debe ser por scope, host gate y capa.
- No copiar codigo ni vendorizar dependencias sin ficha, licencia, secret scan y Dependency Adoption Gate.
- No activar Telegram, GitHub companion, Spotify ni canales externos sin `REVIEW`, credenciales seguras y frontera de contenido.
- No permitir memoria autonoma invisible sobre conversaciones privadas sin filtro de privacidad y revision de claims.
- No mover runtime global a un home oculto sin espejo operacional en BRAIN_OS/COMMS; aqui los handoffs visibles son parte del sistema.

## Traduccion a roadmap local

### P0 - Bajo riesgo, alto valor

- Documento de especificacion: `CLAUDIO_PUBLIC_AGENT_RUNTIME_BLUEPRINT`.
- CLI `doctor/status/permissions/budget/memory/tasks`.
- `skills/<name>/SKILL.md` registry publico-seguro con progressive disclosure.
- ActionGate UX con scopes y dry-run por defecto.

### P1 - Implementacion local

- `SecondBrainLite` con tipos, confianza, fuente, caducidad y boundary tags.
- `TaskBoard` persistente con locks y estados por agente.
- `Scheduler` que solo ejecuta tareas locales y reversibles.
- Watchdog local para procesos Claudio/Argus con logs y stop seguro.

### P2 - Solo con review

- Canal Telegram/OPPO.
- GitHub issue/PR companion.
- Servicio al inicio de Windows.
- Publicacion de paquete npm/pip.
- Integracion con proveedores externos adicionales.

## Decision recomendada

Usar Mercury como referencia de producto y arquitectura publica, no como dependencia directa inmediata. La ruta correcta es extraer un "Claudio Lite / BRAIN_OS Agent Runtime" con cuatro promesas publicas:

1. permiso antes de actuar;
2. memoria con evidencia y limites;
3. skills cargadas bajo demanda;
4. continuidad local verificable.

Eso conserva la ventaja propia de MEDIOEVO: `ActionGate`, `ObservationEnvelope`, `R/Phi/Jamming`, curaduria, handoff y frontera publico/privado.

## Evidencia consultada

- README GitHub: `https://github.com/cosmicstack-labs/mercury-agent`
- Architecture: `https://raw.githubusercontent.com/cosmicstack-labs/mercury-agent/main/ARCHITECTURE.md`
- Decisions: `https://raw.githubusercontent.com/cosmicstack-labs/mercury-agent/main/DECISIONS.md`
- Research: `https://raw.githubusercontent.com/cosmicstack-labs/mercury-agent/main/RESEARCH.md`
- Package metadata: `https://raw.githubusercontent.com/cosmicstack-labs/mercury-agent/main/package.json`

