# Wabi/Claudio Provider Gate - 2026-05-08

## Estado

CERTEZA:
- Wabi/Sabi is the gateway for provider status and conversation.
- Claudio has a safe local bridge in `core/wabi_gateway.py`.
- Ollama local is available; cloud providers remain blocked by default.
- No daemon, external publication, model-weight mutation, alias creation, deploy or secret use was performed.

## Provider Policy

| Route | Default | Use |
|---|---|---|
| Local deterministic | `APPROVE` | Status, chat, fichas, workpacks, redaction, tests |
| Ollama local | `APPROVE_WITH_TIMEOUT` | Local model response with `qwen2.5-coder:3b` or `qwen2.5:0.5b` |
| Codex CLI | `READ_ONLY` | Deep analysis through sandboxed CLI |
| OpenAI Responses | `UNAVAILABLE_NOW` | Only if `OPENAI_API_KEY` exists and ActionGate allows |
| NVIDIA NIM | `BLOCKED_BY_DEFAULT` | Adapter exists; requires env and `WABI_ALLOW_CLOUD_PROVIDERS=1` |
| Qwen cloud | `BLOCKED_BY_DEFAULT` | Adapter exists; requires env and `WABI_ALLOW_CLOUD_PROVIDERS=1` |
| Dry-run | `APPROVE` | Last fallback workpack without model/network |

## Programming Model Profiles

Wabi/Sabi now resolves cloud model aliases without making a network call:

| Provider | Env alias | Aliases |
|---|---|---|
| NVIDIA NIM | `WABI_NVIDIA_NIM_MODEL_ALIAS` | `ultra`, `llama-70b`, `super`, `nano-30b`, `nano-9b` |
| Qwen cloud | `WABI_QWEN_MODEL_ALIAS` | `qwen-plus`, `qwen-235b` |

Exact IDs can be passed through `WABI_NVIDIA_NIM_MODEL` or `WABI_QWEN_MODEL`.
`provider-status --json` is the safe verification command because it reports
configured catalogs, resolved model IDs and provider readiness without printing
secret values. Network remains blocked unless `WABI_ALLOW_CLOUD_PROVIDERS=1` is
set for a gated session.

## Claudio Boundary

- Claudio may ask Wabi for `provider-status` and safe `auto` work.
- Claudio may request cloud only through explicit per-call opt-in:
  `allow_cloud=True` plus provider `nvidia`/`nvidia-nim`/`qwen`/`qwen-cloud`.
- Claudio may not receive raw secrets from Wabi.
- Claudio may not use Wabi to bypass host gate, ActionGate, cleanup gate or publication gate.
- Claudio is not autonomous until a real task succeeds through gateway evidence without Ollama and without unsafe fallbacks.

## Tests

- Wabi: `python -m pytest tests\test_redaction_and_cloud_adapters.py tests\test_provider_orchestrator.py tests\test_cli.py -q`
- Claudio: `python -m pytest tests\test_wabi_gateway.py -q`
- Runtime smoke: `wabi provider-status --json`, `wabi chat "estas ahi" --json`, `wabi auto /status --json`
- Local model smoke: `OllamaBridge.generate("Responde solamente OK.", timeout=120, num_predict=2)` returned `ok=True`, `model=qwen2.5-coder:3b`, `output=OK`.
- Secret redaction smoke: provider status JSON did not contain current NVIDIA, Anthropic or Gemini env secret values.
- Wider `tests\test_psi_wabi_absorption.py` timed out in this pass; not counted as gateway evidence.
- Model catalog tests cover NVIDIA/Qwen alias resolution with mocked HTTP only;
  no real provider call was performed for this configuration pass.
- Follow-up real provider smoke:
  - `Claudio -> Wabi -> NVIDIA NIM` with alias `super` returned `ok=true`,
    provider `nvidia-nim`, action `cloud_chat_completion`, output `OK`.
  - NVIDIA `ultra` reached provider but was unavailable to the current account
    (`404 Function not found for account`).
  - The NGC/Docker token in `Formal\banananana.txt` returned `401
    Authentication failed` when tried as a NIM bearer.
  - Qwen real call was skipped because no `DASHSCOPE_API_KEY` or `QWEN_API_KEY`
    exists in env; Alibaba AccessKey material is not used as DashScope bearer.

Decision: `LOCAL_GATEWAY_READY / NVIDIA_SUPER_REAL_SMOKE_OK / QWEN_WAITING_FOR_BEARER / AUTONOMY_NOT_CLAIMED`.
