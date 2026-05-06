# Observacionista Local Code Agent Intake - 2026-05-04

Status: `SELECTIVE_ABSORPTION_DONE / RAW_SOURCE_NOT_CANON`

## Source

| field | value |
|---|---|
| source | `C:\Users\L-Tyr\Downloads\New folder\#!usrbinenv python3.txt` |
| exists | yes |
| bytes | `51984` |
| lines | `1094` |
| sha256 | `DE38C80104CDDC3A40CE36490B6232589A510A978FFF80041FB0624EBEEB5564` |
| curador decision | `NEEDS_FICHA_BEFORE_USE` |
| reason | new path has only partial/name-only matches against older `Downloads\#!usrbinenv python3.txt` intake |

## Useful Technology Extracted

- `CERTEZA`: the source is a stdlib-only local code agent with command blocking, secret redaction, skipped build/cache dirs, an AGENTS contract, and Observacionismo labels.
- `CERTEZA`: it is not imported wholesale and is not public copy.
- `INFERENCIA`: the useful part for the current request is not the full repair engine; it is the local conversational/pending-control pattern with evidence boundaries.
- `INCOGNITA`: the full patching engine still needs separate security review before any code-edit automation is trusted.

## Absorption

Implemented as a smaller Claudio-native local surface:

- `-=MEDIOEVO=-\-=LIBROS\claudio\tools\observacionista_chat.py`
- `-=MEDIOEVO=-\-=LIBROS\claudio\tests\test_observacionista_chat.py`
- `-=MEDIOEVO=-\-=LIBROS\claudio\docs\OBSERVACIONISTA_CHAT_LOCAL_2026-05-04.md`

The new tool reads `qa_artifacts\pending\pending_review_latest.json`, selects only `local_candidate` pending items, keeps private/external/heavy lanes blocked, and can talk through either local Ollama or deterministic evidence summaries.

## Boundary

- Do not delete the raw source yet.
- Do not copy the raw source into open-dev packages.
- Do not enable command execution or patch automation from this source without a separate ActionGate review.
- Do not claim it is a working autonomous engineer beyond the tested conversational/workpack surface.

## Next Gate

Before deleting or archiving this exact source, create a cleanup approval row with this SHA256, verify no newer unique code remains unextracted, and update `DELETE_CANDIDATES.md` or a dated cleanup manifest.
