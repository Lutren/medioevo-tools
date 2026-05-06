# Curador Always-On Protocol

Status: `ACTIVE_FRAMEWORK_RULE`

Purpose: prevent every agent from creating new residue when it finds dirty
repos, duplicated folders, Downloads sources, external projects, legacy code or
unknown technical material.

## Rule

Every unknown source must be classified before it is used.

No source is copied, published, archived, deleted, promoted to product or left
as chat-only context until it has one of these outcomes:

| outcome | meaning | required artifact |
|---|---|---|
| `REGISTERED_EXISTING` | already has a ficha or registry entry | cite the registry path and line |
| `TECH_EXTRACT_CANDIDATE` | contains useful implementation or architecture | add backlog/ficha, hash, tests or smoke plan |
| `PRIVATE_OR_BLOCKED` | private, secret-like, paid, RPG/TCG or unsafe | register boundary, do not copy to open lanes |
| `DISCARD_CANDIDATE` | not useful or generated residue | add to `DELETE_CANDIDATES.md`; no direct deletion |
| `ARCHIVE_CANDIDATE` | useful history but not active | add to migration/archive map before moving |

## Preflight Command

Use:

```powershell
python tools\release\curador_preflight.py --path <path>
```

From Claudio, the wrapper is:

```powershell
python tools\curador_preflight.py --path <path>
```

The tool is read-only. It checks existing registries, detects obvious technical
signals and prints a ficha template when the path is undocumented.

Workspace audit can include the same classifier for discovered Git roots:

```powershell
python tools\release\audit_repo.py --curador-preflight-git-roots --curador-limit 20 --json
```

## Ficha Before Absorption

Minimum fields:

| field | required content |
|---|---|
| `path` | exact local path or repo URL |
| `hash/evidence` | SHA256, commit, test output, API proof or line reference |
| `classification` | `OPEN`, `COMMERCIAL`, `BOOKS_EDITORIAL`, `PRIVATE`, `ARCHIVE`, `UNKNOWN_REVIEW_REQUIRED` |
| `useful_tech` | `CERTEZA`, `INFERENCIA`, `INCOGNITA` |
| `extraction_mode` | `IDEA_ONLY`, `SELECTIVE_ABSORPTION_ONLY`, `RUNTIME_DEP`, `DO_NOT_USE` |
| `target_lane` | package, app, research lane, Claudio doc, memory vault or `DELETE_CANDIDATES` |
| `claim_boundary` | what cannot be claimed publicly |
| `private_boundary` | what cannot be copied |
| `validation` | test, scan, smoke, compile or reason for no test |

## Copy Rule

Useful material is copied only in the smallest safe form:

1. Prefer a summary, interface, schema, test fixture or minimal extracted module.
2. Preserve provenance with hash, source path and decision.
3. Run secret/path/claim/license review before any public lane.
4. Keep dirty repos, vendors, raw Downloads and private material out of packages.

## Discard Rule

`Deshechar` means:

1. document why it is not useful;
2. list the path in `DELETE_CANDIDATES.md`, `DUPLICATES_AND_DEAD_CODE.md` or an archive map;
3. only delete or move after the cleanup gate, path containment check and evidence.

Silent deletion is not a curator action.

## Claudio Integration

Claudio agents must treat this as part of the FCU:

- before touching broad/dirty repositories;
- before importing external code or dependencies;
- before cleaning cache/residue;
- before promoting any raw source into `core`, `runtime`, `packages`, `apps` or public GitHub;
- before closing a task that discovered new material.

The residue left by the agent is part of the task. A task is not closed while
new unregistered sources or discard candidates remain undocumented.

Harness skill: `tools/harness/skills/curador-operativo/SKILL.md`.

## Validation 2026-05-03

- `python -m py_compile tools\release\curador_preflight.py` -> OK.
- `python -m py_compile tools\curador_preflight.py` from Claudio -> OK.
- `python tools\release\curador_preflight.py --path tools\claw-code --json` -> registered existing tech review, detected `rust_package`, Git clean.
- `python tools\curador_preflight.py --path docs\CURADOR_ALWAYS_ON_CLAUDIO_2026-05-03.md --json` -> registered existing Claudio doc.
- `python tools\release\audit_repo.py --curador-preflight-git-roots --curador-limit 3 --json` -> audit runner emits `curador_git_roots`.
- Focused secret scan over docs, AGENTS, product/visibility maps, harness skill and Claudio wrapper/doc -> `count_reported=0`.
- Focused scan over `CLAUDE.md`, `NEXT_SESSION_BRIEF.md` and `PENDIENTES_MASTER.md` -> `count_reported=0`.

Note: `tools\release\curador_preflight.py` lives under the internal release
tooling path. The release scanner marks `tools/release` as `denylist path` by
policy; this blocks packaging the tool as a release artifact but does not block
using it locally.
