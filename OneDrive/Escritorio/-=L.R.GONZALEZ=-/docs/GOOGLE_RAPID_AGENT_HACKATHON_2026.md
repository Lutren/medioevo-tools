# Google Rapid Agent Hackathon 2026

Status: `PUBLIC_REPO_LIVE / CLOUD_BLOCK`

Date: 2026-05-01

## Verified Public Facts

- Hackathon: Google Cloud Rapid Agent Hackathon.
- Devpost: `https://rapid-agent.devpost.com/`
- Dates: May 5 to Jun 11, 2026.
- Prize pool: 60,000 USD.
- Requirement: functional agent powered by Gemini and Google Cloud Agent Builder.
- Requirement: meaningful MCP integration with at least one participating partner solution.
- Submission requires hosted project URL, public open-source repository, approximately 3 minute demo video and completed Devpost form.
- Judging criteria include technological implementation, design, potential impact and quality of idea.

## Chosen Lane

`hackathons/google-rapid-agent-2026`

Project name: `Agent Safety Gate for Real Work`.

Core idea: an agent that plans a real release or operations task, collects partner MCP evidence, writes an observation envelope and returns a human-supervised `APPROVE`, `REVIEW` or `BLOCK` handoff packet.

## Why This Is The Right Entry

- It matches the user's thesis: agents should accomplish real tasks, but with evidence and human control.
- It is public-safe: no private prompts, full Claudio orchestration, MEDIOEVO canon, RPG/TCG, family data or secrets.
- It is product-aligned: it advertises the open layer while preserving deeper implementation, integrations and consulting as paid work.
- It can target a partner track: GitLab MCP first; Arize, Dynatrace, MongoDB, Elastic or Fivetran as fallbacks once final details are published.

## Local Evidence

- `python -m rapid_agent_guardian.cli examples\release_goal.json --out runtime\demo_packet.json` -> OK.
- `python -m rapid_agent_guardian.readiness --out runtime\submission_readiness.json` -> `decision=LOCAL_PUBLIC_SAFE`, `cloudDemoReady=false`.
- `python scripts\export_public_repo.py` -> `publish_staging\hackathons\google-rapid-agent-2026-public-safe`, `decision=PUBLIC_EXPORT_STAGED`.
- `python -m unittest discover -s tests` -> 3 tests OK.
- `python -m unittest discover -s tests` after exporter -> 4 tests OK.
- `python tools\release\scan_secrets.py --path hackathons\google-rapid-agent-2026 --json --fail-on-findings` -> `count_reported=0`.
- `python tools\release\scan_secrets.py --path publish_staging\hackathons\google-rapid-agent-2026-public-safe --json --fail-on-findings` -> `count_reported=0`.
- Public repo created from the clean staging only: `https://github.com/Lutren/rapid-agent-guardian`.
- Initial public commit: `511333d576aa9f0273d1134390786b8cb8255e02`.
- Export metadata tightening commit: `9de50f23502ada7934c1e61bde54699da20c553d`.
- Remote repo verification: visibility `PUBLIC`, default branch `main`.
- Remote `.github/FUNDING.yml`: present and points to `Lutren`.
- Repo homepage points to `https://github.com/sponsors/Lutren`.
- Repo topics: `agent-safety`, `ai-agents`, `audit-trail`, `gemini`, `google-cloud`, `human-in-the-loop`, `mcp`, `release-engineering`.

## Local Host State

- `gcloud` CLI is not installed.
- `google-genai` Python package is installed.
- `google-adk` and `google-cloud-aiplatform` were not detected in the active Python environment.
- `runtime\submission_readiness.json` mantiene bloqueada la demo cloud hasta configurar Google Cloud CLI y endpoint MCP real.

## Next Actions

1. Join Devpost manually if not already joined.
2. On or after May 5, read final partner resource details and credits instructions.
3. Install Google Cloud CLI.
4. Create a fresh Google Cloud project for the hackathon.
5. Apply credits before enabling billable services.
6. Enable Vertex AI / Agent Builder.
7. Choose partner MCP based on final official partner resources.
8. Deploy hosted demo via Agent Builder, ADK, Cloud Run or the path required by the hackathon.
9. Keep the public repo scoped to the exported hackathon package only.
10. Record a 3 minute demo video.

## Publication Boundary

Do not publish the whole workspace. The live public repo is:

- `https://github.com/Lutren/rapid-agent-guardian`

It was created only from the local staged public export:

- `publish_staging\hackathons\google-rapid-agent-2026-public-safe`
- `publish_staging\hackathons\google-rapid-agent-2026-public-safe\PUBLIC_EXPORT_MANIFEST.json`

Only publish a clean repo derived from:

- `hackathons/google-rapid-agent-2026/README.md`
- `LICENSE`
- `pyproject.toml`
- `rapid_agent_guardian/`
- `scripts/export_public_repo.py`
- `examples/`
- `tests/`
- `docs/HACKATHON_PLAN.md`
- `docs/SUBMISSION_DRAFT.md`

Exclude:

- `runtime/`
- secrets and local auth;
- private canon;
- RPG/TCG paths;
- vendors, caches and build outputs.
