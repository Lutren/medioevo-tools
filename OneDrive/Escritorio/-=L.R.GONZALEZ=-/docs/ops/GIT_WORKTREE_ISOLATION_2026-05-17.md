# Git Worktree Isolation - 2026-05-17

Estado: aislamiento local para evitar commits amplios. No se ejecuto `git add`,
`git commit`, `git reset`, `git checkout`, `git clean`, push ni deploy.

## Snapshot

- Comando: `git status --short`
- Resultado resumido: `total=547`, `modified=77`, `untracked=470`, `other=0`.
- Lectura: el workspace ya estaba sucio antes de este cierre y no es apto para
  `git add .` ni commit amplio.

## Write set de este cierre

Rutas intencionales:

- `PENDIENTES_MASTER.md`
- `docs/ops/PENDIENTES_MASTER_RECONCILIATION_2026-05-17.md`
- `docs/ops/GIT_WORKTREE_ISOLATION_2026-05-17.md`
- `docs/publishing/BOOK_RELEASE_REVIEW_PACKET_DERIVA_FRAGMENTOS_CALIBRACION_2026-05-17.md`
- `ACTION_GATES.md`
- `DECISIONS.md`
- `TASKS.md`
- `ASSUMPTIONS.md`
- `RISKS.md`
- `TEST_REPORT.md`
- `NEXT_SESSION_BRIEF.md`
- `SESSION_FINGERPRINT.json`
- `docs/pending/PENDING_REVIEW_2026-05-17.md`
- `docs/pending/PENDING_REVIEW_LATEST.md`
- `qa_artifacts/pending/pending_review_2026-05-17.json`
- `qa_artifacts/pending/pending_review_latest.json`
- `-=MEDIOEVO=-/-=LIBROS/claudio/runtime/observacionista/active_workpack.json`
- `-=MEDIOEVO=-/-=LIBROS/claudio/runtime/observacionista/active_workpack.md`

## Reglas para commit futuro

- No usar `git add .`.
- Antes de commit, revisar `git diff -- <ruta>` solo sobre el write set de este
  cierre.
- Excluir todo cambio no relacionado, especialmente `apps/local/wabi-sabi`,
  `COMMS`, `MEDIOEVO_LIVE_TREE`, `publish_staging`, rutas privadas y archivos de
  runtime no generados por este cierre.
- Si se requiere commit, hacerlo path-scoped y con `PublicationGate=BLOCK`.
