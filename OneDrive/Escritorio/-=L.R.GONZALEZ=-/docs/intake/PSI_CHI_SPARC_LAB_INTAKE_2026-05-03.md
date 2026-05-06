# PSI Chi SPARC Lab Intake 2026-05-03

Status: `RESEARCH_ONLY_WITH_CLAIM_BOUNDARY`

This ficha registers the local sources used for the PSI Chi SPARC falsifier run.
It is provenance for local analysis, not permission to publish scientific claims.

## Sources

| source | exists | bytes | lines | sha256 | classification | allowed use |
|---|---:|---:|---:|---|---|---|
| `C:\Users\L-Tyr\Downloads\psi_chi_lab_v8.py` | yes | 33795 | 904 | `6EC65FDAD3FF8FEB6086AB518E51CD9C540EDE450DE8B2C1100E1C367E98EB63` | LOCAL_RESEARCH_FALSIFIER_SCRIPT | Derive `psi_chi_lab_v9.py` locally; keep outputs as evidence only. |
| `C:\Users\L-Tyr\data\Rotmod_LTG.zip` | yes | 110737 | n/a | `0A80CC90714828CC28B7DD57923576714D209F2490328C087C4A4AD607FAF588` | SPARC_ROTATION_CURVE_DATASET | Local leaderboard and cross-validation only; cite dataset/source before any public claim. |

## Boundaries

- `CERTEZA`: The files exist locally and have the hashes above.
- `CERTEZA`: Previous v8 local run found `rar` ahead of `psichi` on SPARC BIC and cross-validation.
- `INFERENCIA`: v9 can be used as a stricter comparison harness by adding MOND variants and NFW baselines.
- `INCOGNITA`: Scientific interpretation remains provisional until the code, fitting procedure, priors and dataset citation are independently reviewed.

## Curator Decision

- Do not copy this script into public packages as proof of a theory.
- Do not publish `psi_chi` as validated physics from these runs.
- Preserve outputs as local falsification evidence.
- If useful code graduates, extract only the tested harness structure with a `CLAIMS.md` and dataset citation.
