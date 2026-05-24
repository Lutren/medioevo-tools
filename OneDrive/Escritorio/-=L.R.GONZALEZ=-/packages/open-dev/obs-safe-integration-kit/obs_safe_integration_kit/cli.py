from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import ObservationEnvelope, EstadoPSI
from .gates import ActionGate, ActionProposal
from .security_workbench import (
    SecurityAction,
    build_security_dry_run,
    build_security_handoff,
    build_security_report,
    default_security_tool_catalog,
    parse_security_fixture,
    validate_security_scope,
)
from .storage import EvidenceStore


def _load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="obs-safe", description="Safe Observacionista integration kernel")
    parser.add_argument("--db", default="obs_evidence.sqlite", help="SQLite evidence store path")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_obs = sub.add_parser("observe-text", help="Store a manual/code/test observation")
    p_obs.add_argument("--source", required=True)
    p_obs.add_argument("--title", default="")
    p_obs.add_argument("--url", default="")
    p_obs.add_argument("--mode", default="manual")
    p_obs.add_argument("--text", default="")
    p_obs.add_argument("--file", default="")

    p_action = sub.add_parser("gate-action", help="Gate an action proposal without executing it")
    p_action.add_argument("--tool", required=True)
    p_action.add_argument("--intent", required=True)
    p_action.add_argument("--args-json", default="{}")
    p_action.add_argument("--shell", action="store_true")
    p_action.add_argument("--network", action="store_true")
    p_action.add_argument("--writes-files", action="store_true")
    p_action.add_argument("--external-effect", action="store_true")

    p_claim = sub.add_parser("claim", help="Register a claim tied to observation evidence")
    p_claim.add_argument("--observation-id", required=True)
    p_claim.add_argument("--claim", required=True)
    p_claim.add_argument("--confidence", type=float, default=0.5)

    sub.add_parser("security-tools", help="List defensive security workbench tools and default gates")

    p_scope = sub.add_parser("security-scope-validate", help="Validate a security ScopeRecord JSON file")
    p_scope.add_argument("--scope-file", required=True)

    p_dry = sub.add_parser("security-dry-run", help="Build a no-execution security dry-run plan")
    p_dry.add_argument("--tool", required=True)
    p_dry.add_argument("--scope-file", required=True)
    p_dry.add_argument("--mode", required=True)

    p_fixture = sub.add_parser("security-parse-fixture", help="Parse a synthetic security fixture with redaction")
    p_fixture.add_argument("--tool", required=True)
    p_fixture.add_argument("--fixture", required=True)

    p_report = sub.add_parser("security-report", help="Generate a fixture-only security report and handoff")
    p_report.add_argument("--fixture", required=True)
    p_report.add_argument("--scope-file", required=True)
    p_report.add_argument("--tool", default="nikto")
    p_report.add_argument("--mode", default="fixture")

    sub.add_parser("status", help="Show store status")

    args = parser.parse_args(argv)

    if args.cmd == "observe-text":
        store = EvidenceStore(args.db)
        text = args.text
        if args.file:
            text = Path(args.file).read_text(encoding="utf-8")
        obs = ObservationEnvelope(source=args.source, title=args.title, url=args.url, mode=args.mode, text=text).finalize()
        psi = EstadoPSI(topic=args.title or args.source)
        psi.absorb_observation(obs)
        oid = store.add_observation(obs)
        store.save_session(psi)
        print(json.dumps({"observation_id": oid, "observation": obs.to_dict(), "psi": psi.to_dict()}, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "gate-action":
        store = EvidenceStore(args.db)
        psi = EstadoPSI(topic=args.intent)
        proposal = ActionProposal(
            tool=args.tool,
            args=json.loads(args.args_json),
            intent=args.intent,
            dry_run=True,
            shell=args.shell,
            network=args.network,
            writes_files=args.writes_files,
            external_effect=args.external_effect,
        )
        decision = ActionGate().evaluate(proposal, psi)
        aid = store.log_action(proposal, decision)
        store.save_session(psi)
        print(json.dumps({"action_id": aid, "decision": decision.to_dict(), "psi": psi.to_dict()}, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "claim":
        store = EvidenceStore(args.db)
        cid = store.add_claim(args.observation_id, args.claim, args.confidence, evidence_ref=args.observation_id)
        print(json.dumps({"claim_id": cid}, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "security-tools":
        catalog = default_security_tool_catalog()
        print(json.dumps({"tools": [tool.to_dict() for tool in catalog.values()]}, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "security-scope-validate":
        decision = validate_security_scope(_load_json(args.scope_file))
        print(json.dumps({"decision": decision.to_dict()}, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "security-dry-run":
        scope = _load_json(args.scope_file)
        action = SecurityAction(tool_id=args.tool, mode=args.mode, target=str(scope.get("target_value", "")))
        plan = build_security_dry_run(action, scope)
        print(json.dumps({"dry_run": plan.to_dict()}, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "security-parse-fixture":
        evidence = parse_security_fixture(args.tool, Path(args.fixture))
        print(json.dumps({"evidence": [item.to_dict() for item in evidence]}, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "security-report":
        report = build_security_report(Path(args.fixture), _load_json(args.scope_file), tool=args.tool, mode=args.mode)
        print(
            json.dumps(
                {
                    "report": report.to_dict(),
                    "handoff": build_security_handoff(report),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if args.cmd == "status":
        store = EvidenceStore(args.db)
        print(json.dumps(store.latest_status(), ensure_ascii=False, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
