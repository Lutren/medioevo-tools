# Formal Secret Provider Intake - 2026-05-08

## Source

| Field | Value |
|---|---|
| Path | `C:\Users\L-Tyr\OneDrive\Escritorio\Formal\banananana.txt` |
| SHA256 | `2FA50B657189AE22D371CFECADC25857770914235CCD3DC2233DFA6EF311D5B2` |
| Bytes | `365` |
| Classification | `PRIVATE_SECRET_CONFIG` |
| Publication gate | `BLOCK_PUBLICATION` |
| Extraction mode | `REDACTED_EVIDENCE_ONLY` |

## Redacted Signals

CERTEZA:
- The file contains provider credential/configuration material related to NVIDIA/NGC.
- This pass detected only redacted signal classes: `nvidia_or_ngc`,
  `docker_login`, `ngc_config` and `aliyun_access_key_style`.
- This pass did not detect a DashScope/Qwen-specific key signal in the file;
  Qwen cloud still expects `DASHSCOPE_API_KEY` or `QWEN_API_KEY` in the
  runtime environment unless a later adapter explicitly supports another
  credential flow.
- The file is useful only as proof that provider setup exists and must be handled by env/vault policy.
- The raw content must not be copied into canon, public docs, prompts, logs, tests or artifacts.

INFERENCIA:
- Wabi/Sabi can support NVIDIA and Qwen style cloud fallback only through secret-safe adapters.
- Claudio should call Wabi/Sabi as a gateway instead of duplicating provider keys across modules.

INCOGNITA:
- Whether the credentials are still active.
- The provider credential material in this file is not suitable as a NVIDIA NIM
  bearer in the current endpoint: a real smoke returned `401 Authentication
  failed`.
- NVIDIA NIM does work from the current environment with alias `super`, but not
  with `ultra` for this account.
- Whether a Qwen/DashScope key exists elsewhere; current Wabi status did not show a configured Qwen-cloud key.

## Boundary

- Do not print values.
- Do not commit values.
- Do not copy raw file content.
- Do not run `docker login`, `ngc config`, package pulls or provider API calls from this intake.
- Do not delete until owner review confirms rotation/obsolescence and cleanup gate approval.

## Implementation Evidence

- `wabi provider-status --json` reports:
  - Ollama local available with `qwen2.5-coder:3b` and `qwen2.5:0.5b`.
  - Codex CLI available in read-only mode.
  - OpenAI Responses unavailable because `OPENAI_API_KEY` is not present.
  - NVIDIA adapter configured by env presence but blocked by default.
  - Qwen cloud adapter present but not configured by env.
  - Cloud calls require `WABI_ALLOW_CLOUD_PROVIDERS=1`.

Decision: `KEEP_PRIVATE_REDACTED_EVIDENCE`.

## Real Smoke Update

- `Formal\banananana.txt` credential material was read only in memory and not
  printed.
- NVIDIA candidate from the file: real NIM call attempted, provider returned
  unauthorized.
- Existing environment NVIDIA credential: real NIM call with alias `super`
  succeeded through Claudio/Wabi.
- Qwen/DashScope: not called because no explicit `DASHSCOPE_API_KEY` or
  `QWEN_API_KEY` is present.

Updated decision: `SECRET_CONFIG_REDACTED / NGC_TOKEN_NOT_NIM_BEARER / NVIDIA_ENV_SUPER_OK / QWEN_MISSING_BEARER`.
