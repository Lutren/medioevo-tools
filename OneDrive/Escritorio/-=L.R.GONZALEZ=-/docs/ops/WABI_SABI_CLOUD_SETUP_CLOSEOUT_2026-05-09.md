# Wabi-Sabi Cloud Setup Closeout - 2026-05-09

Status: `SETUP_VERIFIED / SECRETS_NOT_PRINTED / NO_INSTALL`

## CERTEZA

- Authorized credential source exists:
  `C:\Users\L-Tyr\OneDrive\Escritorio\Formal\bu\banananana.txt`.
- SHA256 of credential source:
  `C5760CEF6CB15E53C395711C92185B53E3443A131131B9452C27231838318FE8`.
- Loader script now points to the real path and loads process/session env vars
  without printing secret values:
  `scripts\set_env_from_banananana.ps1`.
- Wabi-Sabi cloud adapter now includes NVIDIA Integrate aliases:
  `kimi`, `deepseek`, `mistral`, `minimax`, `glm`.
- CLI now accepts those aliases for the deep provider route.
- Cloud calls remain blocked by default unless the session sets
  `WABI_ALLOW_CLOUD_PROVIDERS=1`.

## Live Provider Evidence

Official NVIDIA Integrate model list returned `listed=true` for:

- `moonshotai/kimi-k2.6`
- `deepseek-ai/deepseek-v4-pro`
- `mistralai/mistral-medium-3.5-128b`
- `minimaxai/minimax-m2.7`
- `z-ai/glm4.7`
- `nvidia/nemotron-3-super-120b-a12b`

Minimal Wabi-Sabi live calls:

| alias | provider result | output |
|---|---|---|
| `kimi` | `nvidia-nim:kimi` | `OK` |
| `deepseek` | `nvidia-nim:deepseek` | `OK` |
| `mistral` | `nvidia-nim:mistral` | `OK` |
| `minimax` | `nvidia-nim:minimax` | response captured; includes reasoning text |
| `glm` | `nvidia-nim:glm` | response captured; includes reasoning text |

## Validation

- `python -m py_compile wabi_sabi\cli\main.py wabi_sabi\core\cloud_adapters.py wabi_sabi\core\provider_orchestrator.py`
  -> passed.
- `python -m pytest tests\test_cli.py tests\test_provider_orchestrator.py tests\test_redaction_and_cloud_adapters.py tests\test_safe_executor.py tests\test_task_spec_planner.py -q`
  -> `42 passed`.
- Focused secret scan:
  - `cloud_adapters.py`: `0`
  - `provider_orchestrator.py`: `0`
  - `cli/main.py`: `0`
  - `set_env_from_banananana.ps1`: `1` expected scanner marker because the
    loader contains environment variable names such as `API_KEY` and `SECRET`;
    no secret value was printed or committed.

## How To Use In A Session

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
. .\scripts\set_env_from_banananana.ps1 -Force -EnableCloud
cd .\apps\local\wabi-sabi
.\wabi.cmd auto "responde una prueba corta" --codex-provider kimi --json
.\wabi.cmd auto "responde una prueba corta" --codex-provider deepseek --json
.\wabi.cmd auto "responde una prueba corta" --codex-provider mistral --json
```

For normal safe operation, omit `-EnableCloud`; Wabi-Sabi will keep cloud calls
blocked and use local/Codex/dry-run routes.

## BLOQUEO

- No keys were persisted.
- No model weights were installed or pulled.
- No deploy, push, publication or account action was executed.
- Full autonomous cloud coding remains gated by ActionGate and host state.

Fingerprint: `C5760CEF6-WABI-CLOUD-SETUP`
