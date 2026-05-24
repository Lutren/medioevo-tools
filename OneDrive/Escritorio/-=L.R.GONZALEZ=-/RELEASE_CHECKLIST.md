# RELEASE_CHECKLIST

Estado: local prep only. No autoriza publicacion.

## Global

- [x] `AGENTS.md` existe.
- [x] `README.md` existe.
- [x] `PRODUCT_MAP.md` existe.
- [x] `VISIBILITY_MATRIX.md` existe.
- [x] `RISK_REGISTER.md` existe.
- [x] `DUPLICATES_AND_DEAD_CODE.md` existe.
- [x] `MIGRATION_MAP.md` existe.
- [x] `PRIVATE_BOUNDARY.md` existe.
- [x] `SECRET_SCAN_REPORT.md` existe.
- REVIEW_REQUIRED: Scan global limpio. Estado actual: `NO`,
  `count_reported=223`, `truncated_at=500`. Paquete:
  `docs/security/GLOBAL_SENSITIVE_SCAN_TRIAGE_2026-05-06.md`.
- LEGAL_REVIEW_REQUIRED: Licencia global decidida. Estado actual:
  `LEGAL_REVIEW_REQUIRED`. Paquete:
  `docs/legal/GLOBAL_LICENSE_REVIEW_PACKET_2026-05-06.md`.
- REVIEW_REQUIRED: Worktree limpio o cambios acotados al release target.
  Estado actual: `NO`, hay cambios activos de otros agentes. Paquete:
  `docs/developer/WORKTREE_REVIEW_PACKET_2026-05-06.md`.

## Target Local Validado 2026-05-06: `claudio_direct_local`

- [x] ActionGate especifico del target: `APPROVE_LOCAL_ONLY`;
  publicacion externa queda `BLOCK`.
- [x] Allowlist de archivos:
  `qa_artifacts/release_validation/claudio-direct-local-2026-05-06.json`.
- [x] Denylist aplicada: secretos, privado, vendors, builds, caches y
  publicacion externa excluidos del target.
- [x] Secret scan focalizado con `count_reported=0`.
- [x] Path scrub: `local_only_review`; no es artefacto publico y cualquier
  salida publica requiere copia redactada.
- [x] Claims scan: sin strong claims; solo terminos de frontera local.
- [x] Test/build/smoke del producto.
- [x] Evidencia escrita en `qa_artifacts`.
- [x] Post-action verification si hay accion externa: no aplica, no hubo
  accion externa.

## Antes De Cualquier Target Publico Nuevo

- ActionGate especifico del target publico.
- Allowlist de archivos publicos.
- Denylist aplicada: secretos, privado, vendors, builds, caches.
- Secret scan focalizado con `count_reported=0`.
- Path scrub de copia publica.
- Claims scan publico.
- Test/build/smoke del producto publico.
- Evidencia escrita en `qa_artifacts`.
- Post-action verification si hay accion externa.

## Bloqueos Duros

- No publicar workspace completo.
- No usar glob amplio.
- No tocar juego/TCG.
- No publicar libros completos.
- No push/deploy/Gumroad/redes sin autorizacion explicita y gate actual.

## Fuente Complementaria

- `docs/release/RELEASE_CHECKLIST.md`
- `docs/release/RELEASE_READINESS_SCORE.md`
