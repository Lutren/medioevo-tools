# Wabi-Sabi Fallback Runbook - 2026-05-09

Status: `LOCAL_RUNBOOK_READY / NO_MODEL_INSTALL / NO_SECRET_WRITE`

Purpose: make Wabi-Sabi usable as a local fallback when Codex is unavailable,
without granting uncontrolled computer access, publishing externally, installing
cloud models or storing credentials in the repo.

## Operating Rule

Wabi-Sabi can continue local work only through observed state, ActionGate,
source maps, witness logs and rollback evidence. It is not treated as a claim
of consciousness or true metacognition. The practical mechanism is:

```text
Observe -> retrieve evidence -> propose action -> gate -> execute safely -> verify -> handoff
```

## Interface

Current local commands already support the intended surface:

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi
.\wabi.cmd chat "resume el estado local"
.\wabi.cmd provider-status --json
.\wabi.cmd operator-status --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd patch-plan "crea una funcion segura de ejemplo" --target examples\wabi_fallback_example.py --json
.\wabi.cmd task-spec-plan docs\wabi_task_spec.example.json --json
.\wabi.cmd worktree-status --json
```

Operational aliases:

- `wabi chat`: fast local conversation.
- `wabi task`: represented by `auto`, `programmer-workpack`, `task-spec-plan`
  and `task-spec-apply`.
- `wabi status`: represented by `provider-status`, `env-status`,
  `operator-status` and `functional-status`.
- `wabi execute`: represented by `patch-apply` / `task-spec-apply` only when
  ActionGate returns `APPROVE`, with rollback and witness logs.

## Provider Policy

Default provider order remains local-first:

1. local deterministic tools;
2. Ollama/base model only when enabled and available;
3. Codex/OpenAI bridge if configured;
4. cloud adapters only when explicitly enabled;
5. dry-run fallback.

Cloud providers such as DeepSeek, Kimi, MiniMax, Mistral, Qwen and NVIDIA/NIM
must be treated as candidates until their current model IDs and API terms are
verified from official provider surfaces. Do not hard-code speculative IDs.
Do not install or pull models from this runbook.

Current local setup supports NVIDIA Integrate/OpenAI-compatible aliases:

```text
kimi      -> moonshotai/kimi-k2.6
deepseek  -> deepseek-ai/deepseek-v4-pro
mistral   -> mistralai/mistral-medium-3.5-128b
minimax   -> minimaxai/minimax-m2.7
glm       -> z-ai/glm4.7
super     -> nvidia/nemotron-3-super-120b-a12b
```

These aliases remain blocked unless the session sets
`WABI_ALLOW_CLOUD_PROVIDERS=1` and the exact action passes review.

Credential rule:

- allowed: environment variables or an external secret manager;
- blocked: storing API keys, tokens, session cookies or account material in
  repo files, docs, logs, screenshots or JSON artifacts.

## Computer-Control Gate

Approved locally:

- read project files;
- build inventories;
- create docs, plans, dry-run patches and source maps;
- write inside selected workspace paths through PatchPlan/SafeExecutor;
- run allowlisted tests such as `python -m pytest` or `python -m py_compile`.

Review required:

- live GitHub, Sponsors, Gumroad, deploys, social posts or browser account edits;
- cloud model provider enablement;
- model pulls, alias creation, deletion or heavy benchmarks;
- anything touching secrets, payments, legal or global machine configuration.

Blocked:

- destructive deletion;
- exfiltration;
- private game/RPG/TCG release;
- publishing raw corpus or raw private theory;
- bypassing host controls;
- printing secrets.

## Corpus Retrieval

Use the corpus as a source-mapped evidence store, not as raw context flooding.

Primary source:

```text
C:\Users\L-Tyr\OneDrive\Escritorio\MEDIOEVO_CORPUS_UNIFICADO\data\source_map.json
C:\Users\L-Tyr\OneDrive\Escritorio\MEDIOEVO_CORPUS_UNIFICADO\data\chunks.jsonl
C:\Users\L-Tyr\OneDrive\Escritorio\MEDIOEVO_CORPUS_UNIFICADO\07_EVIDENCIA_ARCHIVO\COVERAGE_REPORT.md
```

Retrieval rule:

```text
Answer = relevant_chunks + source_map + public_private_boundary + ActionGate
```

Do not load or paste the whole corpus into prompts. Retrieve by topic and
preserve provenance.

## Validation Commands

Run status-only checks first:

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi
python -m pytest tests\test_provider_orchestrator.py tests\test_safe_executor.py tests\test_task_spec_planner.py -q
.\wabi.cmd provider-status --json
.\wabi.cmd chat "estado" --json
.\wabi.cmd patch-plan "crea una funcion segura de ejemplo" --target examples\wabi_fallback_example.py --json
```

No cloud execution is required to pass this runbook. Cloud status can be
reported as unavailable or disabled as long as it does not leak secrets and
falls back safely.

## Completion Criteria

- Wabi-Sabi can answer a local chat/status request.
- Wabi-Sabi can produce a dry-run patch plan.
- A blocked or review-required request is rejected or routed to review.
- Provider status does not print secrets.
- Any file-writing path leaves rollback and witness artifacts.
