# Prompt-Analyzer Base44 Split Ficha - 2026-05-14

## Source

- Path: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\Prompt-Analyzer.zip`
- SHA256: `48FD6D4CEB5E52CECA596279264F2FAB767F3B0F225F98CCCC9C9827E3928B18`
- Size: `105793256` bytes
- Curador preflight: `NEEDS_FICHA_BEFORE_USE`
- ZIP integrity: `zipfile.testzip() == None`

## Classification

- Classification: `UNKNOWN_REVIEW_REQUIRED_BASE44_UPLOAD_SOURCE`
- Intake action: `LOCAL_REPACKAGING_ONLY`
- Public boundary: user-directed upload candidate only; no Codex upload, deploy, push, or publication executed.
- Secret boundary: exclude local repo/cache/build material before upload.

## Generated Artifact

- Output folder: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\Prompt-Analyzer_base44_parts_20260514_195722`
- Manifest: `BASE44_SPLIT_MANIFEST.json`
- README: `README_BASE44_UPLOAD.md`

## Parts

| part | file | files | testzip |
|---|---|---:|---|
| `01_project_core` | `Prompt-Analyzer_base44_part_01_project_core.zip` | 65 | `None` |
| `02_agent_foundry_os` | `Prompt-Analyzer_base44_part_02_agent_foundry_os.zip` | 83 | `None` |
| `03_mockup_sandbox` | `Prompt-Analyzer_base44_part_03_mockup_sandbox.zip` | 69 | `None` |
| `04_attached_assets` | `Prompt-Analyzer_base44_part_04_attached_assets.zip` | 17 | `None` |

## Exclusions

- Excluded files: `30030`
- Kept files: `234`
- Excluded prefixes:
  - `Prompt-Analyzer/.git/`
  - `Prompt-Analyzer/.local/`
  - `Prompt-Analyzer/node_modules/`
  - `Prompt-Analyzer/.next/`
  - `Prompt-Analyzer/dist/`
  - `Prompt-Analyzer/build/`
  - `Prompt-Analyzer/.vercel/`
  - `Prompt-Analyzer/.wrangler/`
  - `Prompt-Analyzer/.claw/`
  - `Prompt-Analyzer/.claude/`
  - `Prompt-Analyzer/.cache/`
  - `Prompt-Analyzer/__pycache__/`

## Evidence

- Original ZIP `testzip`: `None`.
- Output ZIP `testzip`: all four parts `None`.
- Direct sensitive-name hits in output parts: `0`.
- Nested ZIP note: `MEDIOEVO_AGENT_FOLDER_v2_0_1778795588573.zip` contains two scanner/tool filenames with the word `secret`; no direct `.env`, credential, token, `.git`, `.claw`, `.claude`, or `.wrangler` paths were found in generated parts.

## Decision

- `KEEP_REVIEW`: original ZIP remains untouched.
- `APPROVE_LOCAL`: four local Base44 upload parts generated.
- `BLOCK`: Codex did not upload to Base44, deploy, push, publish, or delete source material.
