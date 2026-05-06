from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from _common import ROOT, add_common_args, print_json, rel, validate_root_arg


STAGING_ROOT = ROOT / "publish_staging" / "github-public-sanitized"
GIT_NAME = "L.R. Gonzalez"
GIT_EMAIL = "lutren@users.noreply.github.com"
MIT_LICENSE = """MIT License

Copyright (c) 2026 L.R. Gonzalez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


@dataclass(frozen=True)
class RepoSpec:
    name: str
    summary: str
    license_status: str
    publish_status: str
    allowed_claims: list[str]
    prohibited_claims: list[str]
    private_exclusions: list[str]
    next_steps: list[str]


COMMON_PROHIBITED = [
    "No proof of consciousness.",
    "No new validated physics or solved cosmology claims.",
    "No autonomous safety guarantee.",
    "No medical, therapeutic or biomedical claim.",
    "No access to private Claudio runtime, RPG, books, assets, prompts or sessions.",
]

COMMON_EXCLUSIONS = [
    "Secrets, tokens, credentials, account sessions and browser profiles.",
    "Local machine-specific paths and private external-drive roots.",
    "Raw Downloads texts and raw ZIPs.",
    "Private RPG, TCG, WorldPulse runtime, assets, scenes, scripts and builds.",
    "Full MEDIOEVO books, canon vaults and commercial bundles.",
    "Vendors, pentest repos, caches and build outputs.",
]


REPOS = [
    RepoSpec(
        name="data-curation-observatory",
        summary="Local-first data curation workflow using manifests, technical cards and CERTEZA/INFERENCIA/INCOGNITA reports.",
        license_status="MIT License for this sanitized public skeleton.",
        publish_status="STAGED_LOCAL_ONLY",
        allowed_claims=[
            "Provides generic templates for local data curation.",
            "Helps separate observed evidence, inference and unknowns.",
            "Produces review artifacts without touching input data.",
        ],
        prohibited_claims=COMMON_PROHIBITED + ["No automatic perfect organization claim."],
        private_exclusions=COMMON_EXCLUSIONS + ["User workspace inventories and real private reports."],
        next_steps=[
            "Add a synthetic sample folder.",
            "Add a manifest-generation smoke test.",
            "Run secret scan and path scrub before any push.",
        ],
    ),
    RepoSpec(
        name="residueos-core",
        summary="ActionGate primitives for approve/review/block decisions, residue ledgers and auditable AI action review.",
        license_status="MIT License for this sanitized public skeleton; thresholds remain DEMO_ONLY until calibrated.",
        publish_status="STAGED_LOCAL_ONLY",
        allowed_claims=[
            "Reviews AI actions before execution.",
            "Records decision rationale and residue.",
            "Supports local tests with synthetic payloads.",
        ],
        prohibited_claims=COMMON_PROHIBITED + ["No guarantee that an action is safe in all environments."],
        private_exclusions=COMMON_EXCLUSIONS + ["Commercial integrations and private thresholds."],
        next_steps=[
            "Map from existing open-dev residueos package.",
            "Preserve DEMO_ONLY threshold labels.",
            "Add CLI smoke test.",
        ],
    ),
    RepoSpec(
        name="ai-web-gateway-observacionista",
        summary="Evidence-envelope gateway for API, reader and browser observations with routing, retries, caching and MCP-facing interfaces.",
        license_status="MIT License for this sanitized public skeleton.",
        publish_status="STAGED_LOCAL_ONLY",
        allowed_claims=[
            "Defines an ObservationEnvelope contract.",
            "Separates source observation from research orchestration.",
            "Documents retry, cache and credential boundaries.",
        ],
        prohibited_claims=COMMON_PROHIBITED + ["No unsupervised browser action or credential automation by default."],
        private_exclusions=COMMON_EXCLUSIONS + ["Credential vault values, browser profiles and live account automation."],
        next_steps=[
            "Start with whitepaper and schema tests.",
            "Keep browser action disabled until ActionGate exists.",
            "Add MCP schemas with synthetic fixtures.",
        ],
    ),
    RepoSpec(
        name="obs-info-kernel-lite",
        summary="Lightweight claim registry and evidence-store toolkit for labeling evidence gaps, anti-information and dark-information candidates.",
        license_status="MIT License for this sanitized public skeleton.",
        publish_status="STAGED_LOCAL_ONLY",
        allowed_claims=[
            "Helps label claims, evidence and gaps.",
            "Uses synthetic corpus examples.",
            "Keeps research and product claims separated.",
        ],
        prohibited_claims=COMMON_PROHIBITED + ["No hidden-truth detector or proof engine claim."],
        private_exclusions=COMMON_EXCLUSIONS + ["Raw research corpus and private synthesis texts."],
        next_steps=[
            "Extract only low-claim primitives.",
            "Add synthetic corpus fixtures.",
            "Run claims scan before public README.",
        ],
    ),
    RepoSpec(
        name="observational-calibration-toolkit",
        summary="Operational calibration schemas, falsifier templates and null-model examples for observer-aware workflows.",
        license_status="MIT License for this sanitized public skeleton.",
        publish_status="STAGED_LOCAL_ONLY",
        allowed_claims=[
            "Defines operational R, Phi_eff and J_c labels.",
            "Provides falsifier and null-model templates.",
            "Supports reproducible synthetic examples.",
        ],
        prohibited_claims=COMMON_PROHIBITED + ["No claim that operational R is physical entropy."],
        private_exclusions=COMMON_EXCLUSIONS + ["Private theory notes and non-public datasets."],
        next_steps=[
            "Add JSON schema for technical cards.",
            "Add tests for example reports.",
            "Keep mathematical claims operational and scoped.",
        ],
    ),
    RepoSpec(
        name="duat-lab",
        summary="Synthetic DUAT laboratory skeleton for residue, calibration, event-store and artifact-memory experiments.",
        license_status="MIT License for this sanitized public skeleton.",
        publish_status="STAGED_LOCAL_ONLY_RESEARCH_BOUNDARY",
        allowed_claims=[
            "Provides a synthetic lab pattern for observer-state experiments.",
            "Separates event logging from artifact promotion.",
            "Documents residue, calibration and falsifier boundaries.",
        ],
        prohibited_claims=COMMON_PROHIBITED
        + [
            "No claim that DUAT validates cosmology, consciousness or new physics.",
            "No RPG, MEDIOEVO canon, WorldPulse runtime or private game material.",
        ],
        private_exclusions=COMMON_EXCLUSIONS
        + [
            "DUAT raw Downloads texts.",
            "MEDIOEVO RPG scenes, scripts, lore, assets and WorldPulse runtime.",
            "Private DUAT/canon notes that have not been sanitized.",
        ],
        next_steps=[
            "Add a minimal synthetic event-store fixture.",
            "Add artifact graph and calibration schema examples.",
            "Run claims scan for physics/cosmology language before public README.",
        ],
    ),
    RepoSpec(
        name="neurostate-ui",
        summary="Local observability UI skeleton for agent-state experiments, split from mixed NEUROSTATE source notes.",
        license_status="MIT License for this sanitized public skeleton; source imports remain excluded until split and sanitized.",
        publish_status="STAGED_LOCAL_ONLY_SPLIT_REQUIRED",
        allowed_claims=[
            "Documents a local UI concept for observing agent-state variables.",
            "Keeps model connectors gated and local by default.",
            "Provides privacy-first notes before any implementation.",
        ],
        prohibited_claims=COMMON_PROHIBITED
        + [
            "No medical, psychological or cognitive diagnostic claim.",
            "No autonomous control over Ollama, LM Studio or browser actions without ActionGate.",
        ],
        private_exclusions=COMMON_EXCLUSIONS
        + [
            "Raw NEUROSTATE HTML/JS/CSS from Downloads until split review.",
            "Local model lists, prompts, sessions and account data.",
        ],
        next_steps=[
            "Split UI, runtime and pitch sections into separate technical cards.",
            "Add privacy notes and local-only connector boundary.",
            "Add a static synthetic demo before any runtime integration.",
        ],
    ),
    RepoSpec(
        name="la-biblioteca-de-alejandria",
        summary="Public index for sanitized repositories, boundaries, whitepapers and support links.",
        license_status="MIT License for this sanitized public skeleton.",
        publish_status="STAGED_LOCAL_ONLY",
        allowed_claims=[
            "Indexes public-safe repositories and whitepapers.",
            "Explains open, commercial, editorial and private boundaries.",
            "Points to Sponsors and product surfaces after verification.",
        ],
        prohibited_claims=COMMON_PROHIBITED + ["No promise that private works are included."],
        private_exclusions=COMMON_EXCLUSIONS + ["Paid products, full books, RPG and private roadmaps."],
        next_steps=[
            "Link only to verified public URLs.",
            "Add boundary map.",
            "Keep private work summarized, not copied.",
        ],
    ),
]


def run(command: list[str], cwd: Path) -> dict[str, object]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    return {
        "command": command,
        "cwd": rel(cwd),
        "returncode": result.returncode,
        "stdout_tail": result.stdout.splitlines()[-12:],
        "stderr_tail": result.stderr.splitlines()[-12:],
    }


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def repo_files(spec: RepoSpec) -> dict[str, str]:
    readme = f"""# {spec.name}

{spec.summary}

Status: `{spec.publish_status}`. This staging repo is local-only until current
secret scan, path scrub, claims scan and ActionGate approval pass.

## What This Includes

{bullets(spec.allowed_claims)}

## What This Excludes

See `PRIVATE_EXCLUSIONS.md`.

## License

{spec.license_status}

## Next Steps

{bullets(spec.next_steps)}
"""
    claims = f"""# CLAIMS

## Allowed Claims

{bullets(spec.allowed_claims)}

## Prohibited Claims

{bullets(spec.prohibited_claims)}
"""
    exclusions = f"""# PRIVATE_EXCLUSIONS

The following material must not enter this public repo:

{bullets(spec.private_exclusions)}
"""
    security = """# SECURITY

Do not commit secrets, tokens, credentials, account sessions, real customer data
or private workspace inventories.

Before any public push:

- run secret scan;
- run path scrub;
- run claims scan;
- verify license text;
- verify ActionGate approval.
"""
    license_text = MIT_LICENSE
    whitepaper = f"""# Whitepaper Draft

## Summary

{spec.summary}

## Technical Card

| field | value |
|---|---|
| repo | `{spec.name}` |
| status | `{spec.publish_status}` |
| license | {spec.license_status} |
| fixtures | synthetic only |
| private boundary | see `PRIVATE_EXCLUSIONS.md` |

## Validation

Public release requires tests or reproducible demo, secret scan, path scrub,
claims scan and ActionGate approval.
"""
    return {
        "README.md": readme,
        "CLAIMS.md": claims,
        "PRIVATE_EXCLUSIONS.md": exclusions,
        "SECURITY.md": security,
        "LICENSE": license_text,
        "docs/WHITEPAPER_DRAFT.md": whitepaper,
    }


def stage_repo(spec: RepoSpec, *, write: bool, init_git: bool, skip_existing: bool) -> dict[str, object]:
    target = STAGING_ROOT / spec.name
    row: dict[str, object] = {"repo": spec.name, "target": rel(target), "publish_status": spec.publish_status}
    if target.exists() and skip_existing:
        row["skipped"] = "target_exists"
        return row
    if target.exists() and any(target.iterdir()):
        row["ok"] = False
        row["reason"] = "target exists and is not empty"
        return row
    files = repo_files(spec)
    row["files"] = sorted(files)
    if not write:
        row["ok"] = True
        row["dry_run"] = True
        return row

    target.mkdir(parents=True, exist_ok=True)
    for relative, content in files.items():
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8", newline="\n")

    commands: list[dict[str, object]] = []
    if init_git:
        commands.extend(
            [
                run(["git", "init", "-b", "main"], target),
                run(["git", "config", "user.name", GIT_NAME], target),
                run(["git", "config", "user.email", GIT_EMAIL], target),
                run(["git", "add", "--", *sorted(files)], target),
                run(["git", "diff", "--cached", "--check"], target),
            ]
        )
        if all(command["returncode"] == 0 for command in commands):
            commands.append(run(["git", "commit", "-m", "Initial sanitized public staging"], target))
        commands.append(run(["git", "status", "--short"], target))
        commands.append(run(["git", "remote", "-v"], target))
    row["commands"] = commands
    row["ok"] = all(command["returncode"] == 0 for command in commands) if commands else True
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage public-sanitized GitHub repo skeletons without external publication.")
    add_common_args(parser)
    parser.add_argument("--repo", choices=[spec.name for spec in REPOS], action="append")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--init-git", action="store_true")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    validate_root_arg(args)

    selected = [spec for spec in REPOS if not args.repo or spec.name in args.repo]
    results = [stage_repo(spec, write=args.write, init_git=args.init_git, skip_existing=args.skip_existing) for spec in selected]
    data = {
        "staging_root": rel(STAGING_ROOT),
        "external_actions_performed": False,
        "write": args.write,
        "init_git": args.init_git,
        "repos": [spec.name for spec in selected],
        "results": results,
        "ok": all(item.get("ok") or item.get("skipped") == "target_exists" for item in results),
    }
    if args.write:
        out_dir = ROOT / "qa_artifacts" / "release_validation"
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / "github-public-sanitized-staging.json"
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        data["written"] = rel(target)
    if args.json:
        print_json(data)
    else:
        for item in results:
            status = "skip" if item.get("skipped") else "ok" if item.get("ok") else "failed"
            print(f"{item['repo']}: {status} -> {item['target']}")
        if args.write:
            print(f"wrote {data['written']}")
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
