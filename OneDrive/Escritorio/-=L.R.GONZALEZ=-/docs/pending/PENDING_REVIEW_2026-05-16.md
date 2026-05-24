# Pending Review - 2026-05-16

Status: generated snapshot. This file is evidence for triage, not proof that old checkboxes are still valid and not permission to publish, push, deploy or delete.

## Counts

- Active markdown raw open items: `18`.
- Active markdown deduplicated open items: `18`.
- Claudio `PENDIENTES_MASTER.md` raw open items: `0`.
- Claudio deduplicated open items: `0`.

## Active Markdown By Priority

| priority | dedup_count |
| --- | --- |
| P1 | 1 |
| UNCLASSIFIED | 17 |

## Active Markdown By Lane

| lane | dedup_count |
| --- | --- |
| commercial | 3 |
| general | 12 |
| research_claims | 1 |
| runtime_claudio | 1 |
| website_marketing | 1 |

## Active Markdown By Blocker

| blocker | dedup_count |
| --- | --- |
| external_or_gated | 7 |
| host_or_heavy | 2 |
| legal_or_human | 1 |
| local_candidate | 6 |
| private_boundary | 2 |

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
| UNCLASSIFIED | general | local_candidate | Review metodologica WDI antes de interpretar comparabilidad o resultados predictivos. | PENDIENTES_MASTER.md:6 | 1 |
| UNCLASSIFIED | general | local_candidate | Resolver o aislar el arbol git sucio antes de cualquier commit path-scoped. | PENDIENTES_MASTER.md:10 | 1 |
| UNCLASSIFIED | general | local_candidate | Si se continua MTS, crear siguiente evaluacion solo con preregistro previo y sin modificar modelo, labels ni holdout. | PENDIENTES_MASTER.md:11 | 1 |
| UNCLASSIFIED | general | local_candidate | Uso de sensores reales, datos personales, telemetria, camara, microfono, ubicacion o biometria en MTS. | PENDIENTES_MASTER.md:17 | 1 |
| UNCLASSIFIED | general | local_candidate | Optional code classifier solo si encaja con tests existentes. | TASKS.md:38 | 1 |
| UNCLASSIFIED | commercial | host_or_heavy | `HOST-STARTUP-NEXT-LOGIN-CHECK`: despues del proximo inicio de Windows, verificar que no aparezcan nuevas ventanas visibles y que `ClaudioBootSupervisor` siga con resultado `0`. | -=MEDIOEVO=-/-=LIBROS/claudio/TASKS.md:77 | 1 |
| UNCLASSIFIED | commercial | private_boundary | Review comercial de Deriva, Fragmentos y Calibracion: titulo, orden, descripcion, keywords, categoria y precio. | PENDIENTES_MASTER.md:7 | 1 |
| UNCLASSIFIED | commercial | external_or_gated | Publicacion, upload, deploy, git push, Gumroad, KDP, redes o ZIP publico. | PENDIENTES_MASTER.md:15 | 1 |
| UNCLASSIFIED | general | external_or_gated | Completar assets locales para los tres libros candidatos: export EPUB/KPF/PDF/DOCX, portada KDP/public-ready y checklist de tienda. | PENDIENTES_MASTER.md:8 | 1 |
| UNCLASSIFIED | general | host_or_heavy | Mantener los otros 31 libros como backlog etiquetado por asset/status hasta cierre de export/cover/metadata/price/store. | PENDIENTES_MASTER.md:9 | 1 |
| UNCLASSIFIED | general | private_boundary | Exposicion de manuscritos privados, canon privado, secretos, tokens o rutas sensibles. | PENDIENTES_MASTER.md:16 | 1 |
| UNCLASSIFIED | general | external_or_gated | Confirmar proveedor/proyecto antes de deploy externo del paquete limpio. | TASKS.md:15 | 1 |
| UNCLASSIFIED | general | external_or_gated | Separar cambios previos del worktree fuente antes de cualquier commit/deploy desde source. | TASKS.md:16 | 1 |
| UNCLASSIFIED | general | external_or_gated | Revision humana final antes de compartir la variante `PUBLIC_SAFE` externamente. | TASKS.md:29 | 1 |
| UNCLASSIFIED | research_claims | legal_or_human | Review legal/humana de World Bank/WDI antes de redistribucion o claim externo. | PENDIENTES_MASTER.md:5 | 1 |
| UNCLASSIFIED | runtime_claudio | external_or_gated | `HOST-REVIEW-CLEARANCE`: bajar `disk_pct` por debajo de `85` y revisar RPC `135` con PowerShell/admin/firewall antes de declarar host `APPROVE`. | -=MEDIOEVO=-/-=LIBROS/claudio/TASKS.md:80 | 1 |
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
