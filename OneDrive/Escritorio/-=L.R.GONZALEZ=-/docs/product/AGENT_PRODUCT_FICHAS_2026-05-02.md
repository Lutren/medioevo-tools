# AGENT_PRODUCT_FICHAS_2026-05-02

Decision aplicada: `open core + UI paga`, con direccion visual `ciudad de agentes`.

Este registro ordena los productos como fichas operativas. La corrida limitada
del 2026-05-02 publico targets concretos con evidencia; cualquier salida nueva
sigue bloqueada por secret scan, path scrub, claims scan, frontera privada,
pruebas, licencia y ActionGate.

## Regla base

| carril | se puede abrir | se vende / protege |
|---|---|---|
| OPEN_CORE | schemas, SDKs, falsadores, fixtures sinteticos, docs public-safe, CLIs y ejemplos sin datos privados | soporte, integracion, hosting, auditorias, plantillas premium |
| COMMERCIAL_AGENT_UI | no publicar fuente completa por defecto | UI pulida, wrapper agente, instalador, soporte, packs Gumroad/website |
| INTERNAL_RESEARCH | papers low-claim y datasets sinteticos despues de revision | corpus crudo, claims fuertes, rutas locales, experimentos privados |
| PRIVATE_IP | nada por defecto | RPG, TCG, lore, assets, libros completos, runtime privado |

## Fichas comerciales / agentes

| producto | ficha tecnica | ficha comercial | ficha agente | estado |
|---|---|---|---|---|
| FlujoCRM | `apps\commercial\flujocrm`; Electron, `better-sqlite3`, `chart.js` local, lockfile, smoke local, source ZIP y Windows QA installer reconstruidos; app instalada abre UI completa desde `mockup.html`; UI escribe contactos a SQLite via IPC y E2E verifica `stage`, `value`, `last_activity` | venta Windows-first por Gumroad/website; standalone antes de bundle; fuente privada por defecto | `Agente Mercado`: organiza clientes, pipeline, recordatorios, evidencia de notas CRM y acciones reversibles | FOUNDER_ACCESS_SQLITE_QA; falta clean VM, firma o aviso unsigned y legal final |
| Asistente Negocio | `apps\commercial\asistente-negocio`; Electron sin deps runtime pesadas; assets GEODIA incluidos; source ZIP, Windows NSIS installer, portable ZIP, icon, package-final QA, notas de instalacion y installed-app E2E verificados | producto comercial para negocios pequenos; Windows founder access manual; no prometer envio automatico | `Agente Mostrador`: prepara respuestas WhatsApp/correo para aprobacion humana | FOUNDER_ACCESS_WINDOWS_QA; soporte/privacidad/reembolso en draft; falta clean VM, firma o aviso unsigned aprobado y legal final |
| Mini Office | `apps\commercial\mini-office`; app Python/HTML local, runtime HTTP corregido, `npm test` real, server smoke y ZIP fuente verificados | vender solo despues de limpiar copy; hoy no usar Gumroad publico por claims/corrupcion/licencia ambigua | `Agente Oficina`: copywriter, designer, creative y operaciones de productividad | LOCAL_SMOKE_QA / COPY_CLAIMS_BLOCK; falta limpiar README/landing/install scripts, resolver licencia y re-test |
| Argus Desktop | `apps\commercial\argus-desktop`; React/Vite/Electron, CodeMirror, markdown, PWA/capacitor | app premium/interna para usuarios Claudio; puede ser wrapper central | `Agente Consola`: chat, ciudad, vision, studio, evidence, anthill y runtime Claudio | REVIEW; auditar rutas locales, UX y limite public-safe |
| Wave FC | `docs\product\wave-collapse.md`, `website\wave-collapse.html`; demo local document-collapse | producto de curaduria documental, auditoria y rollback; vender setup/plantillas | `Agente Curador Documental`: ordena, reduce ruido, conserva evidencia y rollback | LOCAL_DEMO_READY / PUBLICATION_BLOCK |
| MEDIOEVO Agent Ops Pack | `packages\paid\medioevo-agent-ops-pack`; ZIP Gumroad `7cf8fdf5...` | plantillas premium, checklists y workflow para creadores/investigadores | `Agente Curador Datos`: `CERTEZA / INFERENCIA / INCOGNITA`, manifiestos y rutas de siguiente agente | PUBLICADO_GUMROAD; mantener hash, soporte y website |
| NEUROSTATE Dashboard | split futuro desde `#!usrbinenv python3.txt` y staging `neurostate-ui` | paid setup/dashboard local; open UI minimal como lead | `Agente Estado`: observa estado de agentes/workflows, no diagnostica personas | BLOCKED_BY_SPLIT; privacidad y claims review |
| DUAT Templates | DUAT Genesis publico + plantillas premium; DUAT Geodia queda privado | vender templates sinteticos y laboratorio guiado; no vender prueba fisica/cosmologica ni motor Geodia | `Agente Laboratorio`: event store, artifact graph, calibracion, falsadores y memoria de experimentos | REVIEW; Genesis ya existe con tests; falta staging public-safe y plantillas |
| GEODIA OMNIS | `duat_omnis_v1.py` y fichas DUAT/GEODIA; simulacion social sintetica sin dependencias externas | interno/privado; no vender prediccion social ni publicar ingenieria | `Agente Sociometro`: explora escenarios sinteticos, residuo, recursos, cultura y conflicto | PRIVATE_LAB_REVIEW; convertir a fixture privado reproducible |

## Fichas open core

| producto | ficha tecnica | que se abre | que queda fuera | claims |
|---|---|---|---|---|
| ResidueOS | `packages\open-dev\residueos`; gate local, SQLite, CLI/API, tests | action gate, decision envelope, fixtures sinteticos | runtime privado, datasets reales, metricas comerciales | PUBLICADO_GITHUB; `DEMO_ONLY` hasta calibracion real |
| obsai-core | `packages\open-dev\obsai-core`; primitivas Observacionismo/PSI-IA | residue, regimen, gate, fingerprint, simulacion, CLI | canon/libro/RPG/lore, weights, claims fuertes | PUBLICADO_GITHUB; `DEMO_ONLY` / `RESEARCH_ONLY` |
| observacionismo-gate | `packages\open-dev\observacionismo-gate`; SDK Python MIT | evidence, jamming, cost policy, ejemplos | runtime Claudio, prompts privados | PUBLICADO_GITHUB; low-claim SDK |
| OBS Safe Integration Kit | `packages\open-dev\obs-safe-integration-kit`; ObservationEnvelope, EstadoPSI, ActionGate, EvidenceStore, wrappers y CLI | kernel local-first, adaptadores dry-run, SQLite ledger, ejemplos sinteticos y docs de frontera | ejecucion shell/browser/red, runtime privado, fuentes crudas, credenciales reales | PUBLICADO_GITHUB; engineering-only |
| DUAT Genesis | `packages\open-dev\duat-genesis`; simulacion sintetica, reportes y falsadores sin dependencias | contratos `GenesisState`, `GenesisRule`, `Observation`, `SimulationRun`, CLI `run/report/falsify` | DUAT Geodia privado, RPG/TCG, datos reales, medicina/biologia/neurologia validada | OPEN_LOCAL_READY; tests `3 passed`; publicacion externa pendiente de gate |
| Claudio OS Blueprint | `packages\open-dev\claudio-os-blueprint` | blueprint, politicas, scripts/handoff | ISO terminado, QEMU probado, runtime privado | blueprint only |
| Gemma cleanup toolkit | `packages\open-dev\gemma-observacionismo-cleanup` | limpieza/observacion con fixtures sinteticos | pesos, tuning, performance claim | no quality guarantee |
| AI-Web Gateway | staging public-sanitized | ObservationEnvelope, router policy, cache/retry/MCP docs | credenciales, browser actions inseguras, fuentes privadas | gateway spec only |
| obs-info-kernel-lite | staging public-sanitized | claim registry, evidence store, synthetic corpus | corpus crudo, rareza/topologia/conciencia como verdad | research/tooling only |
| data-curation-observatory | staging public-sanitized | plantillas genericas de curador, demo sintetico, manifest schema | datos de usuario, rutas privadas, pack premium | PUBLICADO_GITHUB; workflow local-first |
| observational-calibration-toolkit | staging public-sanitized | schemas R/Phi/Jc, falsadores, tests sinteticos | fisica validada, conciencia, prediccion garantizada | PUBLICADO_GITHUB; calibration demo |
| DUAT Lab | DUAT Genesis + staging public-sanitized + intake DUAT/GEODIA 2026-05-02 | event store, artifact graph, simulator sintetico, falsadores y reportes low-claim | DUAT Geodia privado, RPG/canon/assets, cosmologia/fisica/conciencia validada, MCP con acciones externas | lab low-claim |
| NEUROSTATE UI | staging public-sanitized | UI local de observabilidad de agentes | diagnostico medico/cognitivo, control inseguro | privacy-first demo |

## Fichas private / frontera

| area | ficha tecnica | regla |
|---|---|---|
| RPG / TCG | private RPG root, `-=MEDIOEVO=-\-=LIBROS\metaevo-tcg`, `claudio\tcg`, `runtime\game_bridge` | no copiar assets, escenas, lore ni runtime a open-source o website comercial sin aprobacion explicita |
| Books / canon | `vault_medioevo`, MEDIOEVO outputs, El Observador, PSI/canon | publicar solo samples aprobados; libros completos y vault quedan protegidos |
| Website assets | `claudio\website` con imagenes GEODIA/MEDIOEVO; RPG assets separados | website es superficie comercial; los assets del juego no se usan como fuente publica por defecto |

## Proxima cola ejecutable

1. Cerrar legal/soporte/signing y clean VM para FlujoCRM y Asistente.
2. Limpiar Mini Office copy/claims/licencia o degradarlo a demo interna.
3. Convertir Writer Workbench en paquete founder-access con smoke.
4. Crear una ficha de dependencia por cada paquete externo antes de instalar.
5. Re-skin gradual: FlujoCRM, Asistente, Mini Office y Argus hacia el app shell `Ciudad de agentes`.
6. Generar landings public-safe por agente cuando claim scan y legal esten limpios.
