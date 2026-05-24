# Pending Review - 2026-05-17

Status: generated snapshot. This file is evidence for triage, not proof that old checkboxes are still valid and not permission to publish, push, deploy or delete.

## Counts

- Active markdown raw open items: `10`.
- Active markdown deduplicated open items: `10`.
- Claudio `PENDIENTES_MASTER.md` raw open items: `0`.
- Claudio deduplicated open items: `0`.

## Active Markdown By Priority

| priority | dedup_count |
| --- | --- |
| P1 | 1 |
| UNCLASSIFIED | 9 |

## Active Markdown By Lane

| lane | dedup_count |
| --- | --- |
| commercial | 1 |
| general | 5 |
| runtime_claudio | 1 |
| wave_fc | 2 |
| website_marketing | 1 |

## Active Markdown By Blocker

| blocker | dedup_count |
| --- | --- |
| external_or_gated | 5 |
| host_or_heavy | 1 |
| local_candidate | 3 |
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
| P1 | general | local_candidate | P1 En el proximo handoff real, capturar `prompt_started_at` desde origen y no desde timestamp operativo aproximado. | MEDIOEVO_LIVE_TREE/TASKS.md:77 | 1 |
| UNCLASSIFIED | general | local_candidate | Optional code classifier solo si encaja con tests existentes. | TASKS.md:38 | 1 |
| UNCLASSIFIED | wave_fc | local_candidate | Calibrar gate interpretativo BRAIN_OS para intake real: hoy la captura fisica pasa, pero `Phi_eff_world < 0.60` bloquea integracion cuando la camara entrega frames oscuros. | apps/local/wabi-sabi/TASKS.md:29 | 1 |
| UNCLASSIFIED | commercial | host_or_heavy | `HOST-STARTUP-NEXT-LOGIN-CHECK`: despues del proximo inicio de Windows, verificar que no aparezcan nuevas ventanas visibles y que `ClaudioBootSupervisor` siga con resultado `0`. | -=MEDIOEVO=-/-=LIBROS/claudio/TASKS.md:98 | 1 |
| UNCLASSIFIED | general | external_or_gated | Confirmar proveedor/proyecto antes de deploy externo del paquete limpio. | TASKS.md:15 | 1 |
| UNCLASSIFIED | general | external_or_gated | Separar cambios previos del worktree fuente antes de cualquier commit/deploy desde source. | TASKS.md:16 | 1 |
| UNCLASSIFIED | general | external_or_gated | Revision humana final antes de compartir la variante `PUBLIC_SAFE` externamente. | TASKS.md:29 | 1 |
| UNCLASSIFIED | runtime_claudio | external_or_gated | `HOST-REVIEW-CLEARANCE`: bajar `disk_pct` por debajo de `85` y revisar RPC `135` con PowerShell/admin/firewall antes de declarar host `APPROVE`. | -=MEDIOEVO=-/-=LIBROS/claudio/TASKS.md:101 | 1 |
| UNCLASSIFIED | wave_fc | private_boundary | Revisar `scripts/load_secrets.ps1`, `secret_store.ps1` y helpers de credenciales como `REVIEW_SECRET_HOOK`; no copiar al canon sin captura segura de secretos. | apps/local/wabi-sabi/TASKS.md:32 | 1 |
| UNCLASSIFIED | website_marketing | external_or_gated | Confirmar LinkedIn desde sesion autenticada del propietario. | TASKS.md:17 | 1 |

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
