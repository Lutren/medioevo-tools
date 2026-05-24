# Wabi Qwen Redacted Presence - 2026-05-13

Estado: `QWEN_MISSING_BEARER_CONFIRMED`

## Scope

This check records provider-key presence only. No secret value was printed,
copied, committed or stored.

## Evidence

Command:

```powershell
python -m wabi_sabi.cli.main provider-status --json
```

Relevant redacted result:

```json
{
  "qwen_configured": false,
  "qwen_active_env_key_present": false,
  "nvidia_configured": true,
  "nvidia_enabled": false,
  "qwen_enabled": false,
  "cloud_policy": "blocked_by_default"
}
```

Environment-name presence check:

```json
[
  {"variable": "DASHSCOPE_API_KEY", "present": false},
  {"variable": "QWEN_API_KEY", "present": false}
]
```

Related NVIDIA presence check:

```json
[
  {"variable": "NVIDIA_API_KEY", "present": true},
  {"variable": "NVIDIA_NIM_API_KEY", "present": false},
  {"variable": "NGC_API_KEY", "present": false}
]
```

Prior redacted intake:

- `docs/intake/FORMAL_SECRET_PROVIDER_INTAKE_2026-05-08.md` detected
  `aliyun_access_key_style`, not a DashScope/Qwen bearer.
- That intake already states the raw file must not be copied into canon, public
  docs, prompts, logs, tests or artifacts.

## Decision

The Wabi P1 question is closed:

- `banananana.txt` is not evidence of a DashScope/Qwen bearer.
- The current environment has no `DASHSCOPE_API_KEY` or `QWEN_API_KEY`.
- Qwen cloud remains configured as an adapter but inactive until a proper
  bearer is supplied through env/vault and `WABI_ALLOW_CLOUD_PROVIDERS=1` is
  explicitly gated.

This does not close the P0 of obtaining/approving a real Qwen/DashScope key.
