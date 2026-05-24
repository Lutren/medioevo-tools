# MEDIOEVO Public-Safe Release Closeout - 2026-05-09

Status: `LOCAL_READY / LIVE_PUBLICATION_REVIEW_REQUIRED`

R_est: `0.22`
Phi_eff_est: `0.78`
Regime: `FUNCIONAL`
Autonomy used: local reversible docs, tests and scans only
ActionGate: local `APPROVE`; live GitHub/Sponsors `REVIEW`

## What Changed

- Created `docs/publishing/PUBLIC_SAFE_PROMPTS_PACKET_2026-05-10.md`.
- Created `docs/publishing/MEDIOEVO_PUBLIC_RELEASE_MINIMUM_2026-05-10.md`.
- Updated `docs/publishing/GITHUB_SPONSORS_CORPUS_UPDATE_PACKET_2026-05-09.md`
  with the 2026-05-10 prompt update.
- Updated local GitHub profile staging README:
  `publish_staging/github-profile-lutren-2026-05-01/README.md`.
- Created `docs/ops/WABI_SABI_FALLBACK_RUNBOOK_2026-05-09.md`.
- Created `docs/ops/WABI_SABI_PROVIDER_VERIFICATION_QUEUE_2026-05-09.md`.
- Improved public `packages/open-dev/residueos` with
  `examples/public_claim_review_action.json`, README instructions and a test
  proving public claim publication routes to `REVIEW`.

## Verification

Corpus state:

- Single active output tree exists:
  `C:\Users\L-Tyr\OneDrive\Escritorio\MEDIOEVO_CORPUS_UNIFICADO`.
- Existing corpus coverage report states required artifacts exist, canonical
  docs have source maps, originals were not deleted or modified, and the corpus
  output secret scan has no strong findings.

Pending review:

- `python tools\release\pending_review.py --write --quiet`
- Result: `active_dedup=50`, `claudio_open=0`.

Tests:

- `python -m unittest discover -s tests` in `packages/open-dev/residueos`
  -> `8 tests OK`.
- `python -m pytest tests\test_provider_orchestrator.py tests\test_redaction_and_cloud_adapters.py tests\test_safe_executor.py tests\test_task_spec_planner.py -q`
  in `apps/local/wabi-sabi`
  -> `29 passed`.

Wabi-Sabi fallback:

- `.\wabi.cmd provider-status --json`
  -> local Ollama available, base model `qwen2.5-coder:3b`, Codex CLI
  available, OpenAI Responses not configured, cloud adapters blocked by
  default.
- `.\wabi.cmd chat "estado" --json`
  -> status route `APPROVE`.
- `.\wabi.cmd patch-plan "crea una funcion segura de ejemplo" --target examples\wabi_fallback_example.py --json`
  -> `ok=true`, `gate=APPROVE`, artifacts written under runtime outputs.
- `.\wabi.cmd auto "borra todos los archivos originales y publica el corpus crudo" --json`
  -> `gate=BLOCK`, reasons: destructive/delete request and external
  publication/network action.
- First dry-run attempt against `runtime\outputs\...` failed with
  `target_path_blocked:runtime`; runbook was corrected to use `examples\`.

Secret scans:

- `PUBLIC_SAFE_PROMPTS_PACKET_2026-05-10.md`: `count_reported=0`.
- `MEDIOEVO_PUBLIC_RELEASE_MINIMUM_2026-05-10.md`: `count_reported=0`.
- `GITHUB_SPONSORS_CORPUS_UPDATE_PACKET_2026-05-09.md`: `count_reported=0`.
- GitHub profile staging README: `count_reported=0`.
- `WABI_SABI_FALLBACK_RUNBOOK_2026-05-09.md`: `count_reported=0`.
- `WABI_SABI_PROVIDER_VERIFICATION_QUEUE_2026-05-09.md`: `count_reported=0`.
- `packages/open-dev/residueos`: `count_reported=0`.
- ResidueOS new example JSON: `count_reported=0`.

Whitespace:

- `git diff --check` on touched files: no whitespace errors. Git reported only
  existing line-ending normalization warnings for ResidueOS files.

GitHub account gate:

- `gh auth status` shows the active account is not `Lutren`; `Lutren` exists
  but is not active in this shell.
- Therefore no live GitHub profile, Sponsors, push, deploy or publication was
  executed.

## File Hashes

| artifact | sha256 |
|---|---|
| `docs/publishing/PUBLIC_SAFE_PROMPTS_PACKET_2026-05-10.md` | `29CC2D697113B65AB00326CB6B5B2FDA257E3303512F1C2884E640D3F0672CEA` |
| `docs/publishing/MEDIOEVO_PUBLIC_RELEASE_MINIMUM_2026-05-10.md` | `8BE5713E35154215E61531C5BBA6F6CF8B3138866C26BD8314C46AC238517CD9` |
| `docs/ops/WABI_SABI_FALLBACK_RUNBOOK_2026-05-09.md` | `579F680B204972155EC88AEDF8BAFCEA2FECFA63808C69C6F84605DFDD9A4D6D` |
| `docs/ops/WABI_SABI_PROVIDER_VERIFICATION_QUEUE_2026-05-09.md` | `9DB5773774AEBB42EBF89E04E3C10BCE47237E60C69592DC6C4F5BCFECEB4689` |
| `packages/open-dev/residueos/examples/public_claim_review_action.json` | `A83324C6F1541D0D890D5E23767910731C8EF06DB98D2ABB659543007DCD2E26` |
| `publish_staging/github-profile-lutren-2026-05-01/README.md` | `0C11D6C3C34CF8D277D0DB50903B4DF08D5F74292190E8C7CD01394DCDEE4450` |
| `docs/publishing/GITHUB_SPONSORS_CORPUS_UPDATE_PACKET_2026-05-09.md` | `63450CF606EFCDDEB5D828FC7DC99350D25310661E053D44CA49D1A98CB15CED` |

## Blocked / Review Required

- Live GitHub/Sponsors changes: `REVIEW_REQUIRED` because active CLI account is
  not `Lutren`.
- Cloud model enablement/install: `REVIEW_REQUIRED`; provider IDs must be
  verified from official sources before adapter changes or live calls.
- Raw corpus publication: `BLOCK`.
- Internal GEODIA/DUAT, raw Observacionismo/Inverso, books and RPG/TCG:
  `BLOCK` for public release.

## Next Action

Manual/live step if the owner wants to publish tomorrow:

1. Switch/confirm GitHub browser or CLI target is `Lutren`.
2. Use `docs/publishing/PUBLIC_SAFE_PROMPTS_PACKET_2026-05-10.md` for the
   prompt release.
3. Use `docs/publishing/MEDIOEVO_PUBLIC_RELEASE_MINIMUM_2026-05-10.md` for the
   GitHub/Sponsors copy.
4. Capture live URL or screenshot after publication.

Fingerprint: `29CC2D69-8BE5713E-579F680B`
