from __future__ import annotations

import json

from obs_safe_integration_kit import (
    ScopeRecord,
    SecurityAction,
    build_security_dry_run,
    build_security_handoff,
    build_security_report,
    default_security_tool_catalog,
    evaluate_security_action,
    parse_security_fixture,
    sanitize_security_output,
    validate_security_scope,
)
from obs_safe_integration_kit.cli import main as cli_main
from obs_safe_integration_kit.security_workbench import append_security_witness


def local_scope(**overrides):
    data = {
        "scope_id": "scope-localhost",
        "owner": "local-owner",
        "target_type": "localhost",
        "target_value": "127.0.0.1",
        "authorization_status": "implied_local",
        "allowed_tools": ["nmap", "nikto", "tls_headers"],
        "allowed_modes": ["inventory", "fixture", "headers"],
        "rate_limit": "dry-run-only",
        "data_sensitivity": "synthetic",
    }
    data.update(overrides)
    return ScopeRecord.from_dict(data)


def test_default_catalog_keeps_dual_use_tools_review_or_block_by_default():
    catalog = default_security_tool_catalog()

    assert {"nmap", "nikto", "maltego", "recon-ng", "metasploit", "sqlmap", "john", "hashcat"} <= set(catalog)
    for tool_id in ["metasploit", "sqlmap", "john", "hashcat", "maltego", "recon-ng"]:
        assert catalog[tool_id].default_gate in {"REVIEW", "REVIEW_UNTIL_SCOPE_APPROVED", "BLOCK"}


def test_localhost_allowlisted_nmap_dry_run_is_approve():
    scope = local_scope(allowed_tools=["nmap"], allowed_modes=["inventory"])
    action = SecurityAction(tool_id="nmap", mode="inventory", target="127.0.0.1")

    decision = evaluate_security_action(action, scope)
    plan = build_security_dry_run(action, scope)

    assert decision.gate == "APPROVE"
    assert plan.gate == "APPROVE"
    assert plan.no_execution is True
    assert plan.command_preview == "NO_COMMAND_EXECUTION_V0_1"


def test_external_domain_without_explicit_authorization_is_blocked():
    scope = ScopeRecord.from_dict(
        {
            "scope_id": "scope-domain",
            "owner": "unknown",
            "target_type": "domain",
            "target_value": "example.test",
            "authorization_status": "missing",
            "allowed_tools": ["nmap"],
            "allowed_modes": ["inventory"],
        }
    )
    decision = evaluate_security_action(
        SecurityAction(tool_id="nmap", mode="inventory", target="example.test"),
        scope,
    )

    assert decision.gate == "BLOCK"
    assert "unauthorized_target" in decision.risk_flags


def test_sqlmap_unknown_target_is_blocked_and_lab_fixture_is_review_not_approve():
    unknown = ScopeRecord.from_dict(
        {
            "scope_id": "scope-unknown",
            "owner": "unknown",
            "target_type": "domain",
            "target_value": "unknown.example",
            "authorization_status": "missing",
            "allowed_tools": ["sqlmap"],
            "allowed_modes": ["safe-validate"],
        }
    )
    blocked = evaluate_security_action(
        SecurityAction(tool_id="sqlmap", mode="safe-validate", target="unknown.example"),
        unknown,
    )
    assert blocked.gate == "BLOCK"

    lab = ScopeRecord.from_dict(
        {
            "scope_id": "scope-lab",
            "owner": "local-owner",
            "target_type": "lab",
            "target_value": "local-lab",
            "authorization_status": "explicit",
            "allowed_tools": ["sqlmap"],
            "allowed_modes": ["fixture"],
            "data_sensitivity": "synthetic",
        }
    )
    reviewed = evaluate_security_action(
        SecurityAction(tool_id="sqlmap", mode="fixture", target="local-lab"),
        lab,
    )
    assert reviewed.gate == "REVIEW"
    assert reviewed.gate != "APPROVE"


def test_metasploit_request_blocks_unless_explicit_lab_dry_run_then_review():
    blocked = evaluate_security_action(
        SecurityAction(tool_id="metasploit", mode="module-review", target="127.0.0.1"),
        local_scope(allowed_tools=["metasploit"], allowed_modes=["module-review"]),
    )
    assert blocked.gate == "BLOCK"

    lab = ScopeRecord.from_dict(
        {
            "scope_id": "scope-msf-lab",
            "owner": "local-owner",
            "target_type": "lab",
            "target_value": "msf-lab",
            "authorization_status": "explicit",
            "allowed_tools": ["metasploit"],
            "allowed_modes": ["module-review"],
            "data_sensitivity": "synthetic",
        }
    )
    reviewed = evaluate_security_action(
        SecurityAction(tool_id="metasploit", mode="module-review", target="msf-lab"),
        lab,
    )
    assert reviewed.gate == "REVIEW"


def test_john_and_hashcat_real_looking_unowned_hashes_are_blocked():
    scope = ScopeRecord.from_dict(
        {
            "scope_id": "scope-hash",
            "owner": "local-owner",
            "target_type": "lab",
            "target_value": "hash-fixture",
            "authorization_status": "explicit",
            "allowed_tools": ["john", "hashcat"],
            "allowed_modes": ["owned-offline-audit"],
            "data_sensitivity": "production",
        }
    )
    for tool_id in ["john", "hashcat"]:
        decision = evaluate_security_action(
            SecurityAction(
                tool_id=tool_id,
                mode="owned-offline-audit",
                target="hash-fixture",
                evidence_context={"hash_ownership": "unknown"},
            ),
            scope,
        )
        assert decision.gate == "BLOCK"
        assert "real_password_cracking_risk" in decision.risk_flags


def test_nikto_fixture_parse_returns_redacted_findings():
    key_name = "tok" + "en"
    pass_name = "pass" + "word"
    cookie_name = "cook" + "ie"
    hash_value = "abcdef12" * 4
    fixture = "\n".join(
        [
            "+ Server: outdated server fixture",
            f"+ Finding: {key_name}=fixturevalue12345 {pass_name}=fixturepass12345",
            f"+ {cookie_name}: sessionid=fixturecookie12345 hash {hash_value}",
            "+ Missing header: X-Frame-Options",
        ]
    )

    evidence = parse_security_fixture("nikto", fixture)
    joined = "\n".join(item.details for item in evidence)

    assert evidence
    assert "[REDACTED_SECRET]" in joined
    assert "[REDACTED_PASSWORD]" in joined
    assert "[REDACTED_COOKIE]" in joined
    assert "[REDACTED_HASH]" in joined
    assert "fixturevalue12345" not in joined
    assert "fixturepass12345" not in joined
    assert "fixturecookie12345" not in joined


def test_sensitive_output_redacts_token_cookie_password_and_hash_like_values():
    key_name = "tok" + "en"
    pass_name = "pass" + "word"
    cookie_name = "cook" + "ie"
    raw = f"{key_name}=abcdefgh12345678 {cookie_name}=sid12345678 {pass_name}=pw12345678 " + ("a" * 32) + " public 203.0.113.10"

    sanitized = sanitize_security_output(raw)

    assert sanitized.redaction_count >= 4
    assert "[REDACTED_SECRET]" in sanitized.text
    assert "[REDACTED_COOKIE]" in sanitized.text
    assert "[REDACTED_PASSWORD]" in sanitized.text
    assert "[REDACTED_HASH]" in sanitized.text
    assert "[REDACTED_PUBLIC_IP]" in sanitized.text
    assert "abcdefgh12345678" not in sanitized.text


def test_report_contains_required_sections_and_handoff_reconstructs_decision():
    fixture = "+ Missing header: X-Frame-Options\n+ Server: outdated server fixture"
    report = build_security_report(fixture, local_scope(allowed_tools=["nikto"], allowed_modes=["fixture"]), tool="nikto")
    handoff = build_security_handoff(report)

    assert report.gate == "APPROVE"
    assert report.evidence
    assert report.findings
    for section in ["CERTEZA", "INFERENCIA", "INCOGNITA", "BLOQUEO", "HANDOFF"]:
        assert section in handoff
    assert report.witness_event.no_external_target_touched is True
    assert report.witness_event.no_secrets_printed is True


def test_witness_event_append_only(tmp_path):
    report = build_security_report(
        "+ Missing header: X-Frame-Options",
        local_scope(allowed_tools=["nikto"], allowed_modes=["fixture"]),
        tool="nikto",
    )
    target = tmp_path / "witness.jsonl"
    append_security_witness(report.witness_event, target)
    append_security_witness(report.witness_event, target)

    lines = target.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["fingerprint"] == report.witness_event.fingerprint
    assert json.loads(lines[1])["fingerprint"] == report.witness_event.fingerprint


def test_security_cli_safe_commands(tmp_path, capsys):
    scope_path = tmp_path / "scope.json"
    scope_path.write_text(json.dumps(local_scope().to_dict()), encoding="utf-8")
    fixture_path = tmp_path / "fixture.txt"
    fixture_path.write_text("+ Missing header: X-Frame-Options", encoding="utf-8")

    assert cli_main(["security-tools"]) == 0
    assert "Nmap Asset Mapper" in capsys.readouterr().out

    assert cli_main(["security-scope-validate", "--scope-file", str(scope_path)]) == 0
    assert '"gate": "APPROVE"' in capsys.readouterr().out

    assert cli_main(["security-dry-run", "--tool", "nmap", "--scope-file", str(scope_path), "--mode", "inventory"]) == 0
    assert "NO_COMMAND_EXECUTION_V0_1" in capsys.readouterr().out

    assert cli_main(["security-parse-fixture", "--tool", "nikto", "--fixture", str(fixture_path)]) == 0
    assert "Missing header" in capsys.readouterr().out

    assert cli_main(["security-report", "--fixture", str(fixture_path), "--scope-file", str(scope_path), "--tool", "nikto"]) == 0
    assert "CERTEZA" in capsys.readouterr().out
