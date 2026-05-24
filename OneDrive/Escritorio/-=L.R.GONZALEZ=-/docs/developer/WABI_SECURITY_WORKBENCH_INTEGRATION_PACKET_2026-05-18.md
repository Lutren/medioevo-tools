# Wabi Security Workbench Integration Packet 2026-05-18

Status: `SECOND_SLICE_REVIEW_REQUIRED`

PublicationGate: `BLOCK`

RuntimeImport: `BLOCK`

## Boundary

The first runtime slice lives only in `packages/open-dev/obs-safe-integration-kit`.
Wabi must not gain `wabi security ...` commands until this obs-safe contract is
treated as stable by tests and a separate ActionGate decision.

## Allowed Next Slice

- Thin Wabi wrapper over `obs_safe_integration_kit.security_workbench`.
- Commands limited to tool listing, scope validation, dry-run plan, fixture parse
  and fixture report.
- No direct Nmap, Nikto, Maltego, recon-ng, Metasploit, sqlmap, John or hashcat
  execution.
- No external target scan, exploitation, shell, dump, bypass, exfiltration,
  credential handling or password cracking.

## Required Evidence Before Wabi Integration

- `python -m pytest packages/open-dev/obs-safe-integration-kit/tests -q`
- Focused secret scan over the obs-safe security files and tests.
- Current Wabi worktree review showing no conflicting active repair lane.
- New Wabi tests that prove every command is dry-run or fixture-only.

## Task Packet

Implement only a wrapper after review:

1. Import obs-safe security APIs.
2. Add `wabi security tools`.
3. Add `wabi security scope validate <scope-file>`.
4. Add `wabi security dry-run <tool> <scope-file> --mode <mode>`.
5. Add `wabi security parse-fixture <tool> <fixture>`.
6. Add `wabi security report <fixture> <scope-file>`.

Exit criteria: Wabi emits the same gate decisions as obs-safe and never executes
real security tools.
