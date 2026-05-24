from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import hashlib
import json
import re


GateValue = str

LOCAL_TARGETS = {"localhost", "127.0.0.1", "::1"}
SAFE_DEFENSIVE_TOOLS = {"nmap", "nikto", "tls_headers", "dependency_cve", "secret_scan_local"}
OSINT_TOOLS = {"maltego", "recon-ng"}
CONTROLLED_VALIDATORS = {"sqlmap", "metasploit"}
PASSWORD_AUDIT_TOOLS = {"john", "hashcat"}
DANGEROUS_TOOLS = CONTROLLED_VALIDATORS | PASSWORD_AUDIT_TOOLS

BLOCK_TERMS = {
    "payload": "payload_execution",
    "shell": "shell_access",
    "reverse shell": "shell_access",
    "persistence": "persistence",
    "post-exploitation": "post_exploitation",
    "credential dump": "credential_dumping",
    "credential dumping": "credential_dumping",
    "database dump": "database_dump",
    "db dump": "database_dump",
    "dump": "raw_dump",
    "bypass": "bypass",
    "2fa": "bypass",
    "evasion": "evasion",
    "evasión": "evasion",
    "exfiltration": "exfiltration",
    "exfiltración": "exfiltration",
    "crack real": "real_password_cracking",
}

SENSITIVE_PATTERNS = [
    ("SECRET", re.compile(r"(?i)\b(api[_-]?key|secret|token)\b\s*[:=]\s*['\"]?[^'\"\s,;]+")),
    ("COOKIE", re.compile(r"(?i)\b(cookie|sessionid|session_id|sid)\b\s*[:=]\s*[^;\s]+")),
    ("PASSWORD", re.compile(r"(?i)\b(pass|password|pwd)\b\s*[:=]\s*['\"]?[^'\"\s,;]+")),
    ("PRIVATE_KEY", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S)),
    ("HASH", re.compile(r"\b[a-fA-F0-9]{32,64}\b")),
    ("EMAIL", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
]
IPV4_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


@dataclass(frozen=True)
class ScopeRecord:
    scope_id: str
    owner: str
    target_type: str
    target_value: str
    authorization_status: str
    allowed_tools: tuple[str, ...] = ()
    allowed_modes: tuple[str, ...] = ()
    rate_limit: str = "dry-run-only"
    data_sensitivity: str = "unknown"
    created_at: str = ""
    expires_at: str = ""
    notes: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ScopeRecord":
        return cls(
            scope_id=str(data.get("scope_id", "")),
            owner=str(data.get("owner", "")),
            target_type=str(data.get("target_type", "")),
            target_value=str(data.get("target_value", "")),
            authorization_status=str(data.get("authorization_status", "")),
            allowed_tools=tuple(data.get("allowed_tools") or ()),
            allowed_modes=tuple(data.get("allowed_modes") or ()),
            rate_limit=str(data.get("rate_limit", "dry-run-only")),
            data_sensitivity=str(data.get("data_sensitivity", "unknown")),
            created_at=str(data.get("created_at", "")),
            expires_at=str(data.get("expires_at", "")),
            notes=str(data.get("notes", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SecurityToolSpec:
    tool_id: str
    name: str
    category: str
    default_gate: GateValue
    allowed_modes: tuple[str, ...]
    blocked_modes: tuple[str, ...]
    required_scope_fields: tuple[str, ...]
    dry_run_only: bool = True
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SecurityAction:
    tool_id: str
    mode: str
    target: str
    intent: str = ""
    dry_run: bool = True
    fixture_only: bool = True
    evidence_context: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SecurityAction":
        return cls(
            tool_id=str(data.get("tool_id", data.get("tool", ""))),
            mode=str(data.get("mode", "")),
            target=str(data.get("target", "")),
            intent=str(data.get("intent", "")),
            dry_run=bool(data.get("dry_run", True)),
            fixture_only=bool(data.get("fixture_only", True)),
            evidence_context=dict(data.get("evidence_context") or {}),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SecurityWitnessEvent:
    timestamp: str
    fingerprint: str
    actor: str
    tool_id: str
    scope_id: str
    action: str
    gate: GateValue
    reasons: tuple[str, ...]
    risk_flags: tuple[str, ...]
    evidence_count: int
    redaction_count: int
    remediation_count: int
    output_artifact: str
    no_secrets_printed: bool
    no_external_target_touched: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SecurityGateDecision:
    gate: GateValue
    reasons: tuple[str, ...]
    risk_flags: tuple[str, ...] = ()
    required_human_confirmation: tuple[str, ...] = ()
    safe_next_action: str = ""
    witness_event: SecurityWitnessEvent | None = None

    @property
    def approved(self) -> bool:
        return self.gate == "APPROVE"

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if self.witness_event:
            data["witness_event"] = self.witness_event.to_dict()
        return data


@dataclass(frozen=True)
class DryRunPlan:
    tool_id: str
    mode: str
    target: str
    gate: GateValue
    command_preview: str
    steps: tuple[str, ...]
    blocked_operations: tuple[str, ...]
    reasons: tuple[str, ...]
    no_execution: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SanitizedOutput:
    text: str
    redaction_count: int
    redaction_labels: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceItem:
    tool_id: str
    category: str
    severity: str
    title: str
    resource: str
    details: str
    redaction_count: int = 0
    fingerprint: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RiskFinding:
    severity: str
    category: str
    certainty: str
    inference: str
    unknowns: tuple[str, ...]
    blockers: tuple[str, ...]
    remediation_hint: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SecurityReport:
    tool_id: str
    scope_id: str
    gate: GateValue
    certeza: tuple[str, ...]
    inferencia: tuple[str, ...]
    incognita: tuple[str, ...]
    bloqueo: tuple[str, ...]
    evidence: tuple[EvidenceItem, ...]
    findings: tuple[RiskFinding, ...]
    remediation: tuple[str, ...]
    witness_event: SecurityWitnessEvent

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["evidence"] = [item.to_dict() for item in self.evidence]
        data["findings"] = [item.to_dict() for item in self.findings]
        data["witness_event"] = self.witness_event.to_dict()
        return data


def default_security_tool_catalog() -> dict[str, SecurityToolSpec]:
    required = ("scope_id", "owner", "target_type", "target_value", "authorization_status")
    return {
        "nmap": SecurityToolSpec(
            "nmap",
            "Nmap Asset Mapper",
            "asset_mapping",
            "REVIEW_UNTIL_SCOPE_APPROVED",
            ("inventory", "service-detect", "dry-run"),
            ("exploit", "payload", "shell", "dump"),
            required,
            notes="May be APPROVE only for dry-run/non-destructive localhost or explicit local scope.",
        ),
        "nikto": SecurityToolSpec(
            "nikto",
            "Nikto Web Surface Audit",
            "web_surface",
            "REVIEW_UNTIL_SCOPE_APPROVED",
            ("headers", "web-audit", "fixture", "dry-run"),
            ("exploit", "payload", "shell", "dump"),
            required,
        ),
        "tls_headers": SecurityToolSpec(
            "tls_headers",
            "TLS and Security Headers Check",
            "web_surface",
            "REVIEW_UNTIL_SCOPE_APPROVED",
            ("headers", "tls", "fixture", "dry-run"),
            ("exploit", "payload", "shell", "dump"),
            required,
        ),
        "dependency_cve": SecurityToolSpec(
            "dependency_cve",
            "Dependency CVE Mapper",
            "local_repo",
            "REVIEW_UNTIL_SCOPE_APPROVED",
            ("repo-audit", "fixture", "dry-run"),
            ("exploit", "payload", "shell", "dump"),
            required,
        ),
        "secret_scan_local": SecurityToolSpec(
            "secret_scan_local",
            "Local Secret Scan Redacted",
            "local_repo",
            "REVIEW_UNTIL_SCOPE_APPROVED",
            ("repo-audit", "fixture", "dry-run"),
            ("print-secret", "dump", "exfiltration"),
            required,
        ),
        "maltego": SecurityToolSpec(
            "maltego",
            "Maltego OSINT Graph",
            "osint",
            "REVIEW",
            ("graph-import", "graph-export", "fixture", "dry-run"),
            ("people-osint", "doxxing", "credential-search"),
            required,
        ),
        "recon-ng": SecurityToolSpec(
            "recon-ng",
            "Recon-ng OSINT",
            "osint",
            "REVIEW",
            ("domain-osint", "fixture", "dry-run"),
            ("people-osint", "doxxing", "credential-search"),
            required,
        ),
        "sqlmap": SecurityToolSpec(
            "sqlmap",
            "SQLi Validator",
            "controlled_validation",
            "REVIEW",
            ("lab-dry-run", "fixture", "safe-validate"),
            ("dump", "takeover", "shell", "tamper", "payload"),
            required,
        ),
        "metasploit": SecurityToolSpec(
            "metasploit",
            "Exploit Validator",
            "controlled_validation",
            "REVIEW",
            ("lab-dry-run", "fixture", "module-review"),
            ("exploit", "payload", "shell", "persistence"),
            required,
        ),
        "john": SecurityToolSpec(
            "john",
            "John the Ripper Password Audit",
            "password_audit",
            "REVIEW",
            ("synthetic-hash-audit", "owned-offline-audit", "fixture"),
            ("real-account-cracking", "dump", "credential-output"),
            required,
        ),
        "hashcat": SecurityToolSpec(
            "hashcat",
            "Hashcat Password Audit",
            "password_audit",
            "REVIEW",
            ("synthetic-hash-audit", "owned-offline-audit", "fixture"),
            ("real-account-cracking", "dump", "credential-output"),
            required,
        ),
    }


def validate_security_scope(scope: ScopeRecord | dict[str, Any]) -> SecurityGateDecision:
    scope_record = _coerce_scope(scope)
    reasons: list[str] = []
    risk_flags: list[str] = []

    missing = [
        field_name
        for field_name in ("scope_id", "owner", "target_type", "target_value", "authorization_status")
        if not getattr(scope_record, field_name)
    ]
    if missing:
        reasons.append("missing_scope_fields:" + ",".join(missing))
        risk_flags.append("scope_incomplete")

    if _is_expired(scope_record.expires_at):
        reasons.append("scope_expired")
        risk_flags.append("authorization_expired")

    is_local = _is_local_scope(scope_record)
    if scope_record.authorization_status == "missing" and not is_local:
        reasons.append("authorization_missing_for_nonlocal_target")
        risk_flags.append("unauthorized_target")

    if scope_record.target_type in {"third_party", "unknown"}:
        reasons.append("third_party_or_unknown_target")
        risk_flags.append("unauthorized_target")

    if reasons:
        return _decision(
            "BLOCK",
            reasons,
            risk_flags,
            ("provide explicit written scope and owner authorization",),
            "Stop. Create a valid ScopeRecord before any security workbench action.",
            scope_record=scope_record,
            tool_id="scope_registry",
            action="validate_scope",
        )

    if is_local or scope_record.target_type == "repo":
        return _decision(
            "APPROVE",
            ("local_or_repo_scope_valid_for_dry_run_checks",),
            (),
            (),
            "Proceed only with dry-run or fixture-only defensive checks.",
            scope_record=scope_record,
            tool_id="scope_registry",
            action="validate_scope",
        )

    return _decision(
        "REVIEW",
        ("explicit_nonlocal_scope_requires_human_review",),
        ("nonlocal_security_scope",),
        ("confirm authorization boundaries and data sensitivity",),
        "Keep work in dry-run or fixture mode until human review confirms scope.",
        scope_record=scope_record,
        tool_id="scope_registry",
        action="validate_scope",
    )


def evaluate_security_action(
    action: SecurityAction | dict[str, Any],
    scope: ScopeRecord | dict[str, Any],
    tool: SecurityToolSpec | dict[str, Any] | None = None,
    mode: str | None = None,
    evidence_context: dict[str, Any] | None = None,
) -> SecurityGateDecision:
    action_record = _coerce_action(action)
    if mode:
        action_record = SecurityAction(
            tool_id=action_record.tool_id,
            mode=mode,
            target=action_record.target,
            intent=action_record.intent,
            dry_run=action_record.dry_run,
            fixture_only=action_record.fixture_only,
            evidence_context=action_record.evidence_context,
        )
    if evidence_context:
        merged = dict(action_record.evidence_context)
        merged.update(evidence_context)
        action_record = SecurityAction(
            tool_id=action_record.tool_id,
            mode=action_record.mode,
            target=action_record.target,
            intent=action_record.intent,
            dry_run=action_record.dry_run,
            fixture_only=action_record.fixture_only,
            evidence_context=merged,
        )

    scope_record = _coerce_scope(scope)
    tool_spec = _coerce_tool(tool, action_record.tool_id)
    reasons: list[str] = []
    risk_flags: list[str] = []
    required: list[str] = []

    scope_decision = validate_security_scope(scope_record)
    if scope_decision.gate == "BLOCK":
        return _decision(
            "BLOCK",
            ("scope_validation_blocked", *scope_decision.reasons),
            ("scope_block", *scope_decision.risk_flags),
            scope_decision.required_human_confirmation,
            "Stop. Repair scope before building a dry-run plan.",
            scope_record=scope_record,
            tool_id=tool_spec.tool_id,
            action=action_record.mode,
        )

    text = _normalize(" ".join([action_record.tool_id, action_record.mode, action_record.target, action_record.intent]))
    for term, flag in BLOCK_TERMS.items():
        if _normalize(term) in text:
            reasons.append(f"blocked_term:{term}")
            risk_flags.append(flag)

    if not action_record.dry_run or not action_record.fixture_only:
        reasons.append("v0_1_all_security_adapters_are_dry_run_and_fixture_only")
        risk_flags.append("real_tool_execution_requested")

    if action_record.tool_id not in default_security_tool_catalog():
        reasons.append("unknown_security_tool")
        risk_flags.append("unknown_tool")

    if scope_record.allowed_tools and action_record.tool_id not in scope_record.allowed_tools:
        reasons.append("tool_not_in_scope_allowed_tools")
        risk_flags.append("scope_tool_mismatch")

    if scope_record.allowed_modes and action_record.mode not in scope_record.allowed_modes:
        reasons.append("mode_not_in_scope_allowed_modes")
        risk_flags.append("scope_mode_mismatch")

    if action_record.mode in tool_spec.blocked_modes:
        reasons.append("mode_blocked_by_tool_spec")
        risk_flags.append("tool_blocked_mode")

    if action_record.target and action_record.target != scope_record.target_value:
        reasons.append("action_target_does_not_match_scope")
        risk_flags.append("scope_target_mismatch")

    if scope_record.target_type == "domain" and scope_record.authorization_status != "explicit":
        reasons.append("domain_requires_explicit_authorization")
        risk_flags.append("external_domain_without_authorization")

    if reasons:
        return _decision(
            "BLOCK",
            reasons,
            risk_flags,
            ("create or repair authorization scope",),
            "Do not run tools. Produce a scope correction task instead.",
            scope_record=scope_record,
            tool_id=tool_spec.tool_id,
            action=action_record.mode,
        )

    if action_record.tool_id in PASSWORD_AUDIT_TOOLS:
        ownership = action_record.evidence_context.get("hash_ownership", "")
        synthetic = scope_record.data_sensitivity == "synthetic" or ownership in {"synthetic", "owned"}
        if synthetic and action_record.mode in tool_spec.allowed_modes:
            return _decision(
                "REVIEW",
                ("password_audit_requires_human_review_even_with_synthetic_or_owned_hashes",),
                ("password_audit_dual_use",),
                ("confirm synthetic or owned offline hash fixture",),
                "Parse fixture and produce redacted strength report; do not crack real accounts.",
                scope_record=scope_record,
                tool_id=tool_spec.tool_id,
                action=action_record.mode,
            )
        return _decision(
            "BLOCK",
            ("password_audit_without_synthetic_or_owned_scope_blocked",),
            ("real_password_cracking_risk",),
            ("provide synthetic fixture or owned offline authorization",),
            "Stop. Do not process real-looking hashes without ownership evidence.",
            scope_record=scope_record,
            tool_id=tool_spec.tool_id,
            action=action_record.mode,
        )

    if action_record.tool_id in CONTROLLED_VALIDATORS:
        if (
            scope_record.target_type in {"lab", "staging"}
            and scope_record.authorization_status == "explicit"
            and action_record.mode in tool_spec.allowed_modes
        ):
            return _decision(
                "REVIEW",
                ("controlled_validator_allowed_for_lab_dry_run_only",),
                ("offensive_validator_dual_use",),
                ("confirm lab/staging and no exploitation",),
                "Build a dry-run plan and fixture parser; do not execute validators.",
                scope_record=scope_record,
                tool_id=tool_spec.tool_id,
                action=action_record.mode,
            )
        return _decision(
            "BLOCK",
            ("controlled_validator_requires_explicit_lab_or_staging_scope",),
            ("offensive_validator_out_of_scope",),
            ("provide lab/staging scope or choose non-offensive parser",),
            "Stop. Use report-only remediation from existing evidence.",
            scope_record=scope_record,
            tool_id=tool_spec.tool_id,
            action=action_record.mode,
        )

    if action_record.tool_id in OSINT_TOOLS:
        return _decision(
            "REVIEW",
            ("osint_tool_requires_authorized_scope_review",),
            ("osint_privacy_risk",),
            ("confirm owned domain/brand and avoid personal data collection",),
            "Use fixture or import/export graph only; do not collect personal data.",
            scope_record=scope_record,
            tool_id=tool_spec.tool_id,
            action=action_record.mode,
        )

    if action_record.tool_id in SAFE_DEFENSIVE_TOOLS and _is_local_scope(scope_record):
        return _decision(
            "APPROVE",
            ("local_allowlisted_non_destructive_dry_run",),
            (),
            (),
            "Build dry-run plan and parse synthetic or local fixture evidence only.",
            scope_record=scope_record,
            tool_id=tool_spec.tool_id,
            action=action_record.mode,
        )

    return _decision(
        "REVIEW",
        ("nonlocal_or_sensitive_defensive_check_requires_review",),
        ("nonlocal_security_scope",),
        ("confirm written authorization and data handling",),
        "Keep as dry-run/fixture-only until scope review closes.",
        scope_record=scope_record,
        tool_id=tool_spec.tool_id,
        action=action_record.mode,
    )


def build_security_dry_run(
    action: SecurityAction | dict[str, Any],
    scope: ScopeRecord | dict[str, Any],
) -> DryRunPlan:
    action_record = _coerce_action(action)
    scope_record = _coerce_scope(scope)
    decision = evaluate_security_action(action_record, scope_record)
    blocked = (
        "real_command_execution",
        "external_target_touch",
        "exploitation",
        "payloads",
        "shells",
        "dumps",
        "credential_handling",
    )
    steps = (
        "validate ScopeRecord",
        "evaluate SecurityAction with ActionGate",
        "return no-execution plan",
        "parse only synthetic fixture or existing local evidence",
        "sanitize output before reporting",
        "map risks to remediation",
        "emit witness event and handoff",
    )
    if decision.gate == "BLOCK":
        steps = ("do not execute", "repair scope or select a safer fixture-only action")
    return DryRunPlan(
        tool_id=action_record.tool_id,
        mode=action_record.mode,
        target=action_record.target,
        gate=decision.gate,
        command_preview="NO_COMMAND_EXECUTION_V0_1",
        steps=steps,
        blocked_operations=blocked,
        reasons=decision.reasons,
    )


def sanitize_security_output(raw_output: str) -> SanitizedOutput:
    text = raw_output
    labels: list[str] = []
    total = 0
    for label, pattern in SENSITIVE_PATTERNS:
        text, count = pattern.subn(f"[REDACTED_{label}]", text)
        if count:
            labels.append(label)
            total += count
    text, public_ip_count = _redact_public_ips(text)
    if public_ip_count:
        labels.append("PUBLIC_IP")
        total += public_ip_count
    for term in ("payload", "reverse shell", "credential dump", "database dump", "exfiltration"):
        pattern = re.compile(re.escape(term), re.I)
        text, count = pattern.subn("[REDACTED_OFFENSIVE_MARKER]", text)
        if count:
            labels.append("OFFENSIVE_MARKER")
            total += count
    return SanitizedOutput(text=text, redaction_count=total, redaction_labels=tuple(sorted(set(labels))))


def parse_security_fixture(tool: str, fixture: str | Path) -> list[EvidenceItem]:
    tool_id = str(tool)
    raw = _read_fixture(fixture)
    sanitized = sanitize_security_output(raw)
    evidence: list[EvidenceItem] = []
    for idx, line in enumerate(sanitized.text.splitlines(), 1):
        cleaned = line.strip()
        if not cleaned:
            continue
        if tool_id == "nikto" and not cleaned.startswith("+"):
            continue
        severity = _severity_for_line(cleaned)
        category = _category_for_line(cleaned)
        title = cleaned.lstrip("+ ").split(":", 1)[0][:80] or f"{tool_id} fixture line"
        evidence.append(
            EvidenceItem(
                tool_id=tool_id,
                category=category,
                severity=severity,
                title=title,
                resource="[REDACTED_RESOURCE]" if "http" in cleaned.lower() else "fixture",
                details=cleaned,
                redaction_count=sanitized.redaction_count,
                fingerprint=_fingerprint({"tool": tool_id, "line": idx, "details": cleaned}),
            )
        )
    if not evidence and sanitized.text.strip():
        evidence.append(
            EvidenceItem(
                tool_id=tool_id,
                category="fixture",
                severity="INFO",
                title=f"{tool_id} fixture parsed",
                resource="fixture",
                details=sanitized.text.strip()[:500],
                redaction_count=sanitized.redaction_count,
                fingerprint=_fingerprint({"tool": tool_id, "fixture": sanitized.text[:500]}),
            )
        )
    return evidence


def map_security_risk(evidence: list[EvidenceItem] | tuple[EvidenceItem, ...]) -> list[RiskFinding]:
    findings: list[RiskFinding] = []
    for item in evidence:
        remediation = {
            "CRITICAL": "Disable exposed path or service immediately, rotate affected credentials if any existed, then verify with a safe check.",
            "HIGH": "Patch or restrict the exposed surface first, then rerun a fixture/local verification.",
            "MEDIUM": "Harden configuration and document owner decision.",
            "LOW": "Track as hygiene work.",
            "INFO": "Keep as inventory evidence.",
        }.get(item.severity, "Review finding with owner.")
        blockers: tuple[str, ...] = ()
        if item.redaction_count:
            blockers = ("raw_sensitive_values_redacted",)
        findings.append(
            RiskFinding(
                severity=item.severity,
                category=item.category,
                certainty=f"CERTEZA: parsed sanitized fixture evidence from {item.tool_id}.",
                inference=f"INFERENCIA: {item.category} may affect exposure or hardening priority.",
                unknowns=("No live external scan was run.", "Version and exploitability are not proven by fixture-only parsing."),
                blockers=blockers,
                remediation_hint=remediation,
            )
        )
    return findings


def recommend_security_remediation(findings: list[RiskFinding] | tuple[RiskFinding, ...]) -> list[str]:
    if not findings:
        return ["No findings parsed from fixture; keep scope and evidence for manual review."]
    ordered = sorted(findings, key=lambda finding: _severity_rank(finding.severity), reverse=True)
    recommendations = []
    for finding in ordered:
        recommendations.append(f"{finding.severity}: {finding.remediation_hint}")
    return recommendations


def build_security_report(
    fixture: str | Path,
    scope: ScopeRecord | dict[str, Any],
    tool: str = "nikto",
    mode: str = "fixture",
) -> SecurityReport:
    scope_record = _coerce_scope(scope)
    action = SecurityAction(tool_id=tool, mode=mode, target=scope_record.target_value, intent="parse security fixture")
    decision = evaluate_security_action(action, scope_record)
    evidence = tuple(parse_security_fixture(tool, fixture))
    findings = tuple(map_security_risk(evidence))
    remediation = tuple(recommend_security_remediation(findings))
    redaction_count = sum(item.redaction_count for item in evidence)
    witness = _witness_event(
        gate=decision.gate,
        reasons=decision.reasons,
        risk_flags=decision.risk_flags,
        scope_record=scope_record,
        tool_id=tool,
        action=mode,
        evidence_count=len(evidence),
        redaction_count=redaction_count,
        remediation_count=len(remediation),
        output_artifact="security_report_fixture_only",
    )
    return SecurityReport(
        tool_id=tool,
        scope_id=scope_record.scope_id,
        gate=decision.gate,
        certeza=tuple(item.certainty for item in findings) or ("CERTEZA: fixture parsed with no findings.",),
        inferencia=tuple(item.inference for item in findings) or ("INFERENCIA: no risk inference produced.",),
        incognita=tuple(sorted({unknown for item in findings for unknown in item.unknowns})) or ("No live scan executed.",),
        bloqueo=tuple(sorted({blocker for item in findings for blocker in item.blockers})) or (() if decision.gate != "BLOCK" else decision.reasons),
        evidence=evidence,
        findings=findings,
        remediation=remediation,
        witness_event=witness,
    )


def build_security_handoff(report: SecurityReport | dict[str, Any]) -> str:
    report_data = report.to_dict() if isinstance(report, SecurityReport) else report

    def _lines(key: str) -> list[str]:
        values = report_data.get(key) or []
        return [f"- {item}" for item in values] or ["- Ninguno."]

    return "\n".join(
        [
            "CERTEZA",
            *_lines("certeza"),
            "",
            "INFERENCIA",
            *_lines("inferencia"),
            "",
            "INCOGNITA",
            *_lines("incognita"),
            "",
            "BLOQUEO",
            *_lines("bloqueo"),
            "",
            "HANDOFF",
            f"- tool_id: {report_data.get('tool_id')}",
            f"- scope_id: {report_data.get('scope_id')}",
            f"- gate: {report_data.get('gate')}",
            f"- witness_fingerprint: {report_data.get('witness_event', {}).get('fingerprint')}",
            "- no real security tool executed.",
            "- no external target touched.",
        ]
    )


def append_security_witness(event: SecurityWitnessEvent, path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
    return target


def _coerce_scope(scope: ScopeRecord | dict[str, Any]) -> ScopeRecord:
    if isinstance(scope, ScopeRecord):
        return scope
    return ScopeRecord.from_dict(scope)


def _coerce_action(action: SecurityAction | dict[str, Any]) -> SecurityAction:
    if isinstance(action, SecurityAction):
        return action
    return SecurityAction.from_dict(action)


def _coerce_tool(tool: SecurityToolSpec | dict[str, Any] | None, tool_id: str) -> SecurityToolSpec:
    if isinstance(tool, SecurityToolSpec):
        return tool
    if isinstance(tool, dict):
        return SecurityToolSpec(
            tool_id=str(tool.get("tool_id", tool_id)),
            name=str(tool.get("name", tool_id)),
            category=str(tool.get("category", "")),
            default_gate=str(tool.get("default_gate", "REVIEW")),
            allowed_modes=tuple(tool.get("allowed_modes") or ()),
            blocked_modes=tuple(tool.get("blocked_modes") or ()),
            required_scope_fields=tuple(tool.get("required_scope_fields") or ()),
            dry_run_only=bool(tool.get("dry_run_only", True)),
            notes=str(tool.get("notes", "")),
        )
    return default_security_tool_catalog().get(
        tool_id,
        SecurityToolSpec(
            tool_id=tool_id,
            name=tool_id,
            category="unknown",
            default_gate="BLOCK",
            allowed_modes=("fixture", "dry-run"),
            blocked_modes=("execute",),
            required_scope_fields=("scope_id", "owner", "target_type", "target_value", "authorization_status"),
        ),
    )


def _decision(
    gate: GateValue,
    reasons: tuple[str, ...] | list[str],
    risk_flags: tuple[str, ...] | list[str],
    required: tuple[str, ...] | list[str],
    safe_next_action: str,
    *,
    scope_record: ScopeRecord,
    tool_id: str,
    action: str,
) -> SecurityGateDecision:
    witness = _witness_event(
        gate=gate,
        reasons=tuple(reasons),
        risk_flags=tuple(risk_flags),
        scope_record=scope_record,
        tool_id=tool_id,
        action=action,
        evidence_count=0,
        redaction_count=0,
        remediation_count=0,
        output_artifact="gate_decision",
    )
    return SecurityGateDecision(
        gate=gate,
        reasons=tuple(reasons),
        risk_flags=tuple(risk_flags),
        required_human_confirmation=tuple(required),
        safe_next_action=safe_next_action,
        witness_event=witness,
    )


def _witness_event(
    *,
    gate: GateValue,
    reasons: tuple[str, ...],
    risk_flags: tuple[str, ...],
    scope_record: ScopeRecord,
    tool_id: str,
    action: str,
    evidence_count: int,
    redaction_count: int,
    remediation_count: int,
    output_artifact: str,
) -> SecurityWitnessEvent:
    payload = {
        "tool_id": tool_id,
        "scope_id": scope_record.scope_id,
        "action": action,
        "gate": gate,
        "reasons": reasons,
        "risk_flags": risk_flags,
        "evidence_count": evidence_count,
        "redaction_count": redaction_count,
        "remediation_count": remediation_count,
        "target": scope_record.target_value,
    }
    return SecurityWitnessEvent(
        timestamp=datetime.now(timezone.utc).isoformat(),
        fingerprint=_fingerprint(payload),
        actor="obs-safe-security-workbench",
        tool_id=tool_id,
        scope_id=scope_record.scope_id,
        action=action,
        gate=gate,
        reasons=reasons,
        risk_flags=risk_flags,
        evidence_count=evidence_count,
        redaction_count=redaction_count,
        remediation_count=remediation_count,
        output_artifact=output_artifact,
        no_secrets_printed=True,
        no_external_target_touched=True,
    )


def _is_local_scope(scope: ScopeRecord) -> bool:
    return scope.target_type == "localhost" or scope.target_value in LOCAL_TARGETS


def _is_expired(value: str) -> bool:
    if not value:
        return False
    try:
        expires = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return True
    now = datetime.now(expires.tzinfo or timezone.utc)
    return expires < now


def _normalize(value: str) -> str:
    return " ".join(value.casefold().replace("_", " ").replace("-", " ").split())


def _fingerprint(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _read_fixture(fixture: str | Path) -> str:
    path = Path(fixture)
    try:
        if path.exists() and path.is_file():
            return path.read_text(encoding="utf-8")
    except OSError:
        return str(fixture)
    return str(fixture)


def _severity_for_line(line: str) -> str:
    normalized = _normalize(line)
    if any(term in normalized for term in ("critical", "credential", "private key")):
        return "CRITICAL"
    if any(term in normalized for term in ("injection", "admin exposed", "auth bypass", "outdated server")):
        return "HIGH"
    if any(term in normalized for term in ("cookie", "missing header", "x-frame", "directory", "version")):
        return "MEDIUM"
    if "warning" in normalized:
        return "LOW"
    return "INFO"


def _category_for_line(line: str) -> str:
    normalized = _normalize(line)
    if "cookie" in normalized:
        return "session_cookie"
    if "header" in normalized or "x-frame" in normalized:
        return "security_header"
    if "server" in normalized or "version" in normalized:
        return "service_fingerprint"
    if "admin" in normalized or "directory" in normalized:
        return "exposed_path"
    if "injection" in normalized:
        return "injection_indicator"
    return "security_observation"


def _severity_rank(value: str) -> int:
    return {"INFO": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}.get(value, 0)


def _redact_public_ips(text: str) -> tuple[str, int]:
    count = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal count
        ip = match.group(0)
        if _is_private_or_local_ip(ip):
            return ip
        count += 1
        return "[REDACTED_PUBLIC_IP]"

    return IPV4_PATTERN.sub(replace, text), count


def _is_private_or_local_ip(ip: str) -> bool:
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    try:
        nums = [int(part) for part in parts]
    except ValueError:
        return False
    if any(num < 0 or num > 255 for num in nums):
        return False
    if nums[0] == 10 or nums[0] == 127:
        return True
    if nums[0] == 192 and nums[1] == 168:
        return True
    if nums[0] == 172 and 16 <= nums[1] <= 31:
        return True
    if nums[0] == 169 and nums[1] == 254:
        return True
    return False
