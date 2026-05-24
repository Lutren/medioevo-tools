# Wabi-Sabi Provider Verification Queue - 2026-05-09

Status: `LOCAL_SETUP_VERIFIED / NO_INSTALL / SESSION_SECRET_LOAD_ONLY`

Purpose: capture the requested cloud/local model direction for Wabi-Sabi
without installing models, storing credentials or hard-coding unverified model
IDs.

## Rule

Every provider must pass this sequence before Wabi-Sabi can use it for real
programming work:

```text
official provider docs/API -> exact model ID -> terms/cost check -> env var only
-> status-only probe -> mock or dry-run test -> ActionGate -> limited live call
```

No provider is enabled by name alone.

## Candidate Families

| provider family | intended use | status | credential rule |
|---|---|---|---|
| Local Ollama / Qwen coder | fast fallback, local code triage, no-credit continuity | already supported by Wabi-Sabi policy when available | no cloud key |
| NVIDIA / Nemotron | reasoning/code cloud candidate | adapter exists; model catalog must be rechecked before live use | env var only |
| Qwen cloud | reasoning/code cloud candidate | adapter exists; model catalog must be rechecked before live use | env var only |
| DeepSeek | reasoning/code cloud candidate | verification required | env var only |
| Kimi | long-context reasoning/code candidate | verification required | env var only |
| MiniMax | agent/reasoning candidate | verification required | env var only |
| Mistral | code/reasoning/open-weight/provider candidate | verification required | env var only |
| OpenAI / Codex bridge | existing deep route when configured | use only through current bridge and gates | env var only |

## Local Alias Setup

Wabi-Sabi can now route these public model aliases through the NVIDIA Integrate
OpenAI-compatible adapter when credentials are loaded in the current session:

| alias | provider route | model id |
|---|---|---|
| `kimi` | `nvidia-nim` | `moonshotai/kimi-k2.6` |
| `deepseek` | `nvidia-nim` | `deepseek-ai/deepseek-v4-pro` |
| `mistral` | `nvidia-nim` | `mistralai/mistral-medium-3.5-128b` |
| `minimax` | `nvidia-nim` | `minimaxai/minimax-m2.7` |
| `glm` | `nvidia-nim` | `z-ai/glm4.7` |

The aliases are intentionally adapter-level only. They do not install model
weights, persist secrets or enable network calls by default.

## Required Evidence Per Provider

- official docs URL or official API model list response;
- exact model ID observed on 2026-05-09 or later;
- cost/rate-limit notes if visible;
- environment variable name, without value;
- status output proving no secret value is printed;
- mock test or dry-run test;
- ActionGate result before the first live request.

## Provider Enablement Defaults

```text
WABI_ALLOW_CLOUD_PROVIDERS=0
WABI_PROVIDER_ORDER=codex,dry-run
WABI_DISABLE_BASE_MODEL=0
WABI_ENABLE_OLLAMA=0 unless local base model is intentionally selected
```

Cloud calls remain disabled until `WABI_ALLOW_CLOUD_PROVIDERS=1` is set in the
session and the exact provider action passes review.

## Blocked In This Pass

- no pip/npm dependency install;
- no model pull;
- no alias creation;
- no benchmark run against paid APIs;
- no API key printing;
- no provider credentials written to files;

## 2026-05-09 Verification Evidence

- Secret loader read authorized local file
  `C:\Users\L-Tyr\OneDrive\Escritorio\Formal\bu\banananana.txt`.
- Loaded environment variables only in the current process/session.
- Secret values were not printed.
- NVIDIA model list endpoint confirmed these model IDs are listed:
  `moonshotai/kimi-k2.6`, `deepseek-ai/deepseek-v4-pro`,
  `mistralai/mistral-medium-3.5-128b`, `minimaxai/minimax-m2.7`,
  `z-ai/glm4.7`, `nvidia/nemotron-3-super-120b-a12b`.
- Live minimal calls returned successfully through Wabi-Sabi/NVIDIA route:
  `kimi`, `deepseek`, `mistral`, `minimax`, `glm`.
- `minimax` and `glm` can return `reasoning_content`; extractor now preserves
  it when `content` is empty.
- Tests: `42 passed` for CLI/provider/redaction/safe executor/task spec set.

Still blocked by default:

- cloud providers require `WABI_ALLOW_CLOUD_PROVIDERS=1` in the session;
- no provider secrets are persisted by default;
- no broad benchmark or autonomous cloud coding loop was started.

## Next Implementation Step

After official model verification, add provider adapters incrementally:

1. `status()` only, redacted, no network;
2. mocked `execute()` test;
3. disabled-by-default live path;
4. one live status/probe with ActionGate;
5. only then include in `WABI_PROVIDER_ORDER`.
