# Unified Worktree + Observacionista Plan - 2026-05-04

Status: `CANON_DECISION_DOCUMENTED / NO_DELETE_EXECUTED`

## Decision

One active canonical workspace should remain:

```text
C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

Operational runtime stays inside:

```text
C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio
```

Everything outside that root is either intake source, staging, archive, private storage, or deletion candidate after hash/provenance review. No file was deleted or moved in this pass.

## Evidence Snapshot

- Pending review refreshed on `2026-05-04`: `active_dedup=1700`, `claudio_open=52`.
- Current separate repo: `C:\Users\L-Tyr\OneDrive\Documentos\New project 3`.
  - Git: no commits yet on branch `Origen`.
  - Package name: `duat-genesis-observacionista`.
  - Active files excluding `node_modules`, `dist`, `.git`: `43`.
  - Validation: `npm run test -- --run` -> `11 passed`; `npm run build` -> Vite build OK.
  - Key hashes:
    - `package.json`: `24D7A8EB8F24D59F04C3860862387B5F9A1F7308136E2FC99C3CEC80106FBD78`
    - `src\simulation\engine.ts`: `065A48707D5AEA248A40BC3577A6BDF4E155860BBB141ABC169DBB3C38625543`
    - `docs\DUAT_P1_SWEEP_RESULTS.md`: `ADE93F80F024AC2A5D54738D3F920B203E5F35C9CC678D3767AA2CEFAA4772BA`
- Canon public DUAT lane already exists:
  - `packages\open-dev\duat-genesis`
  - classification in `PRODUCT_MAP.md`: `OPEN_PUBLIC_REPO_LIVE`.
  - Validation: `python -m pytest tests -q` -> `3 passed`; `python -m duat_genesis.cli falsify --seed verify --ticks 5` -> 3 falsifiers passed.
- Observacionista local validation:
  - `python -m pytest tests\test_observacionista_chat.py tests\test_puerto_observacionista_local.py -q` -> `7 passed`.
  - `python tools\observacionista_chat.py workpack --write` wrote `runtime\observacionista\active_workpack.json`.

## Root Classifications

| path | current classification | canonical action |
|---|---|---|
| `C:\Users\L-Tyr\Downloads` | registered intake source root | keep as source only; extract selectively |
| `C:\Users\L-Tyr\Downloads\New folder` | new mixed source cluster | needs fichas per file before use |
| `C:\Users\L-Tyr\Downloads\New folder\#!usrbinenv python3.txt` | new local code agent source | selectively absorbed into Claudio chat/workpack tool; raw source not canon |
| `C:\Users\L-Tyr\OneDrive\Documentos\New project 3` | separate Vite/TS DUAT lab worktree | do not keep as separate final worktree; compare and extract unique UI/sweep ideas into one canonical DUAT lane |
| `...\-=MEDIOEVO=-\-=LIBROS\claudio` | Claudio runtime/product root | canonical local runtime, agent, pending and ActionGate surface |
| `...\-=MEDIOEVO=-\CLAUDIO - researchs` | incubator/research | not canonical; extract only tested ideas with source cards |
| `C:\Users\L-Tyr\OneDrive\Escritorio` | desktop control surface | shortcut/access layer only; not source of truth |
| `E:\` | storage/private/research roots | no broad move/delete; preserve `E:\Medioevo_RPG` private boundary |

## One-Version Rule

- DUAT public package: `packages\open-dev\duat-genesis`.
- Claudio local observacionista: `-=LIBROS\claudio\tools\observacionista_chat.py`.
- Pending truth: root `qa_artifacts\pending\pending_review_latest.json` plus Claudio `PENDIENTES_MASTER.md`.
- Curador/source truth: root `SOURCE_INTAKE_REGISTER.md` and dated intake docs.
- Delete truth: `DELETE_CANDIDATES.md` or dated cleanup manifests; no direct deletion by chat.

## Deletion Gate For Later

Before deleting any duplicate worktree/source:

1. Produce hash inventory for the candidate path.
2. Confirm its useful technology is already present in the canonical lane or explicitly rejected.
3. Add a cleanup candidate row with reason, hash, replacement path and boundary.
4. Verify tests/builds for the canonical lane.
5. Only then delete or archive with a dated migration map.

## Immediate Next Workpack

The Observacionista local should work from `local_candidate` pending items only. External/publication/legal/private/heavy tasks stay blocked until ActionGate, host and human review say otherwise.
