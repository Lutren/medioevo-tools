# LIBROS AGENTS FCU Checkbox Reconciliation - 2026-05-13

## Scope

Source: `-=MEDIOEVO=-/-=LIBROS/AGENTS.md`

The priority checklist in that file is an old FCU strategic gate list, not a
verified executable task board. It also contains text corruption such as
`muyales`, `cormuyctos`, `[elichicado]ckout`, `muyndimiento` and `Featumuys`.

## Decision

Convert the section from markdown task checkboxes to explicit gate markers.
This prevents `pending_review` from treating broad, corrupted, external, legal
or host-level items as local actionable backlog.

## Gate Classification

| Item | Gate | Reason |
|---|---|---|
| Verificar payouts reales en plataformas | REVIEW | External platform/account/payment evidence required. |
| Confirmar datos bancarios correctos | REVIEW | Legal/payment/private-account boundary. |
| Fix bugs criticos en checkout | REVIEW | Ambiguous target; checkout/payment surface requires exact repo and QA. |
| VPN/Tor funcionando | REVIEW | Host/network/privacy surface. |
| Deploy medioevo.space actualizado | REVIEW | External deploy/publication action. |
| Publicar contenido en redes | REVIEW | External publication/account action. |
| Enviar aplicaciones a grants/becas | REVIEW | External submission/legal/public identity action. |
| Contactar posibles colaboradores | REVIEW | External communication/action. |
| Optimizar rendimiento Claudio Local | REVIEW | Broad category; requires scoped metric and target before implementation. |
| Mejorar UX del Hub | REVIEW | Broad category; requires scoped surface and QA target. |
| Pipelines de automatizacion | REVIEW | Broad category; requires exact pipeline target. |
| Hardware adicional | REVIEW | Purchase/host-resource decision. |
| Features experimentales | REVIEW | Broad category; not a task without exact feature and acceptance criteria. |
| Investigacion | REVIEW | Broad category; route through intake/claims workflow. |

## Evidence

- `python tools\release\pending_review.py --write --quiet` before this
  reconciliation reported `active_dedup=20`, including 14 `UNCLASSIFIED` items
  from `-=MEDIOEVO=-/-=LIBROS/AGENTS.md`.
- Claudio master backlog was already clean: `claudio_open=0`.

## Operational Rule

These gates do not count as completed work. They remain available as strategic
review prompts, but future executable tasks must live in scoped trackers with
target path, acceptance criteria, ActionGate classification and verification
commands.
