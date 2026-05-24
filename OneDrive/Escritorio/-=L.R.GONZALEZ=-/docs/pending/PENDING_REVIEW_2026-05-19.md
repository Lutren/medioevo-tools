# Pending Review - 2026-05-19

Status: generated snapshot. This file is evidence for triage, not proof that old checkboxes are still valid and not permission to publish, push, deploy or delete.

## Counts

- Active markdown raw open items: `19`.
- Active markdown deduplicated open items: `19`.
- Claudio `PENDIENTES_MASTER.md` raw open items: `0`.
- Claudio deduplicated open items: `0`.

## Active Markdown By Priority

| priority | dedup_count |
| --- | --- |
| P1 | 1 |
| UNCLASSIFIED | 18 |

## Active Markdown By Lane

| lane | dedup_count |
| --- | --- |
| commercial | 1 |
| general | 1 |
| runtime_claudio | 1 |
| wave_fc | 16 |

## Active Markdown By Blocker

| blocker | dedup_count |
| --- | --- |
| external_or_gated | 8 |
| host_or_heavy | 1 |
| legal_or_human | 1 |
| local_candidate | 8 |
| private_boundary | 1 |

## Claudio Master By Priority

| priority | dedup_count |
| --- | --- |

## Claudio Master By Blocker

| blocker | dedup_count |
| --- | --- |

## Top Items

| priority | lane | blocker | item | first evidence | occurrences |
| --- | --- | --- | --- | --- | --- |
| P1 | general | local_candidate | P1 En el proximo handoff real, capturar `prompt_started_at` desde origen y no desde timestamp operativo aproximado. | MEDIOEVO_LIVE_TREE/TASKS.md:87 | 1 |
| UNCLASSIFIED | wave_fc | local_candidate | Proximo: fallback-only v0.3 con fixture local mas realista. | apps/local/wabi-sabi/TASKS.md:11 | 1 |
| UNCLASSIFIED | wave_fc | local_candidate | Calibrar gate interpretativo BRAIN_OS para intake real: hoy la captura fisica pasa, pero `Phi_eff_world < 0.60` bloquea integracion cuando la camara entrega frames oscuros. | apps/local/wabi-sabi/TASKS.md:101 | 1 |
| UNCLASSIFIED | wave_fc | local_candidate | Panel DUAT/Wabi read-only para provider/gate/proposal/patch/test/witness. | apps/local/wabi-sabi/TASKS.md:115 | 1 |
| UNCLASSIFIED | wave_fc | local_candidate | Reiniciar servidor Wabi existente en 8787 solo en accion controlada para cargar el nuevo panel/ruta; v0.2 ya fue probado en servidor temporal 8788. | apps/local/wabi-sabi/TASKS.md:167 | 1 |
| UNCLASSIFIED | wave_fc | local_candidate | Usar `build-assist-plan` en una tarea Wabi pequena con validacion local antes de apply. | apps/local/wabi-sabi/TASKS.md:187 | 1 |
| UNCLASSIFIED | wave_fc | local_candidate | Siguiente paso: agregar contador/presupuesto por sesion para llamadas build-assist cloud desde UI/CLI. | apps/local/wabi-sabi/TASKS.md:198 | 1 |
| UNCLASSIFIED | wave_fc | local_candidate | Siguiente paso: reiniciar servidor UI local y verificar visualmente el panel `Cloud Budget` sin llamada cloud. | apps/local/wabi-sabi/TASKS.md:216 | 1 |
| UNCLASSIFIED | commercial | host_or_heavy | `HOST-STARTUP-NEXT-LOGIN-CHECK`: despues del proximo inicio de Windows, verificar que no aparezcan nuevas ventanas visibles y que `ClaudioBootSupervisor` siga con resultado `0`. | -=MEDIOEVO=-/-=LIBROS/claudio/TASKS.md:98 | 1 |
| UNCLASSIFIED | runtime_claudio | external_or_gated | `HOST-REVIEW-CLEARANCE`: bajar `disk_pct` por debajo de `85` y revisar RPC `135` con PowerShell/admin/firewall antes de declarar host `APPROVE`. | -=MEDIOEVO=-/-=LIBROS/claudio/TASKS.md:101 | 1 |
| UNCLASSIFIED | wave_fc | external_or_gated | Revisar reporte y decidir siguiente ruta: NVIDIA route review, fallback-only coding acceptance o Tree Health panel. | apps/local/wabi-sabi/TASKS.md:22 | 1 |
| UNCLASSIFIED | wave_fc | external_or_gated | Revision manual NVIDIA dashboard/API route antes de v0.6. | apps/local/wabi-sabi/TASKS.md:35 | 1 |
| UNCLASSIFIED | wave_fc | external_or_gated | Crear guia redactada para revisar NVIDIA provider/model not-found. | apps/local/wabi-sabi/TASKS.md:46 | 1 |
| UNCLASSIFIED | wave_fc | private_boundary | Revisar `scripts/load_secrets.ps1`, `secret_store.ps1` y helpers de credenciales como `REVIEW_SECRET_HOOK`; no copiar al canon sin captura segura de secretos. | apps/local/wabi-sabi/TASKS.md:104 | 1 |
| UNCLASSIFIED | wave_fc | external_or_gated | v0.3: live smoke opcional de NVIDIA NIM solo si `WABI_ALLOW_CLOUD_PROVIDERS=1` y el operador habilita el gate. | apps/local/wabi-sabi/TASKS.md:107 | 1 |
| UNCLASSIFIED | wave_fc | external_or_gated | Ejecutar smoke live real de NVIDIA solo cuando `WABI_ALLOW_CLOUD_PROVIDERS=1` este activo en una terminal controlada. | apps/local/wabi-sabi/TASKS.md:113 | 1 |
| UNCLASSIFIED | wave_fc | external_or_gated | Next: UI polish, fallback-only v0.4, or NVIDIA manual route review. | apps/local/wabi-sabi/TASKS.md:125 | 1 |
| UNCLASSIFIED | wave_fc | external_or_gated | Ejecutar live smoke NVIDIA `nano-30b` con prompt sintetico cuando el operador habilite banderas de sesion. | apps/local/wabi-sabi/TASKS.md:177 | 1 |
| UNCLASSIFIED | wave_fc | legal_or_human | Siguiente paso: cablear UI local al `ConversationEngine` o exponer endpoint interno estable para reutilizar `ConversationTurn`. | apps/local/wabi-sabi/TASKS.md:197 | 1 |

## Kairos Fastlane

- Path: `-=MEDIOEVO=-/-=LIBROS/claudio/runtime/observacionista/kairos_attention_hygiene/pendientes_fastlane_2026-05-01.json`.
- Generated at: `2026-05-01T00:08:52+00:00`.
- Stale against this snapshot date: `True`.
- Decision count: `478`.

| action | count |
| --- | --- |
| defer | 325 |
| hold_calibration | 103 |
| queue_next | 50 |

## Operational Rule

At the start of each run/day execute `python tools\release\pending_review.py --write --quiet`, then choose work from shortest verified local closure first. External/publication tasks stay blocked until their specific gate is clean.
