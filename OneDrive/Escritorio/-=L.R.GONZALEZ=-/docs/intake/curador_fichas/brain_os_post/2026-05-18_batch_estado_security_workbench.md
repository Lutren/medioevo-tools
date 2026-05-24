# Ficha Curador - BRAIN_OS POST Batch - estado_security_workbench_post

Status: `FICHADO_BATCH_SELECTIVE_EXTRACTION`

ActionGate: `REVIEW`

PublicationGate: `BLOCK`

RuntimeImport: `BLOCK`

RawAdoption: `BLOCK`

## Source

| field | value |
|---|---|
| path | `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\ESTADO222222222.txt` |
| kind | `.txt` |
| sha256 | `2E118556099DEAE74E07A8CCDC2B6F7D97C9BBBF5828EB2C41BDF244EC1137FE` |
| size_bytes | `18881` |
| classification | `POST_ETHICAL_SECURITY_WORKBENCH_SOURCE` |
| lane | `security` |
| intake_action | `DEFENSIVE_SECURITY_WORKBENCH_INSIGHT_ONLY` |
| target_lane | `packages/open-dev/obs-safe-integration-kit; docs/intake; future Wabi wrapper task packet` |
| action_gate | `REVIEW` |
| publication_gate | `BLOCK` |
| runtime_import | `BLOCK` |
| raw_adoption | `BLOCK` |
| line_count | `547` |
| encoding | `utf-8-sig` |

## Useful Deltas

- Defines MEDIOEVO Ethical Security Workbench as defensive, local-first and owner-authorized.
- Requires ScopeRegistry, Security ActionGate, DryRunPlan, OutputSanitizer, RiskMapper, WitnessLog and Handoff before any tool execution.
- Separates safe defensive checks from OSINT and offensive validators with APPROVE/REVIEW/BLOCK defaults.

## Rejected Material

- Running Nmap, Nikto, sqlmap, Metasploit, John, hashcat, Maltego or recon-ng directly from intake text.
- Scanning third-party targets or external infrastructure without explicit authorization.
- Payloads, shells, dumps, bypass, exfiltration, credential handling or password cracking.
- Adding Wabi CLI commands before the obs-safe contract is tested.

## Claim Boundary

`DEFENSIVE_DRY_RUN_FIXTURE_ONLY_SECURITY_CONTRACT`

Strong terms are not promoted by this ficha. Publication, runtime import and raw adoption stay blocked.

## Term Signals

- `AGI`: count `8`, first lines `[30, 44, 86, 152, 169, 249, 258, 309]`
- `ActionGate`: count `9`, first lines `[5, 58, 138, 152, 193, 206, 328, 483]`
- `Handoff`: count `14`, first lines `[16, 65, 121, 148, 150, 197, 214, 243]`
- `PASS`: count `11`, first lines `[7, 30, 46, 95, 97, 182, 271, 273]`
- `Phi`: count `3`, first lines `[135, 191, 514]`
- `Phi_eff`: count `3`, first lines `[135, 191, 514]`
- `bypass`: count `3`, first lines `[97, 182, 273]`
- `cookie`: count `2`, first lines `[348, 501]`
- `dump`: count `9`, first lines `[30, 45, 93, 182, 257, 269, 270, 356]`
- `exfiltración`: count `3`, first lines `[30, 92, 274]`
- `hashcat`: count `11`, first lines `[7, 21, 30, 46, 152, 180, 259, 326]`
- `john`: count `11`, first lines `[7, 21, 30, 46, 152, 179, 259, 326]`
- `maltego`: count `7`, first lines `[7, 28, 42, 129, 155, 175, 255]`
- `metasploit`: count `12`, first lines `[7, 21, 30, 44, 152, 158, 177, 258]`
- `nikto`: count `10`, first lines `[7, 26, 41, 129, 152, 157, 174, 249]`
- `nmap`: count `10`, first lines `[7, 26, 40, 129, 152, 154, 173, 248]`
- `password`: count `7`, first lines `[7, 30, 46, 95, 271, 346, 501]`
- `payload`: count `4`, first lines `[265, 354, 468, 502]`
- `publicación`: count `2`, first lines `[96, 276]`
- `publication`: count `1`, first lines `[517]`
- `recon-ng`: count `7`, first lines `[7, 28, 42, 129, 156, 176, 256]`
- `secret`: count `12`, first lines `[5, 26, 96, 195, 252, 275, 343, 408]`
- `shell`: count `5`, first lines `[30, 94, 182, 266, 503]`
- `sqlmap`: count `14`, first lines `[7, 21, 30, 45, 129, 152, 159, 178]`
- `token`: count `2`, first lines `[344, 501]`

## ZIP Internal Entries

- Not a ZIP container.

## Evidence

- Hash computed from exact source path on 2026-05-18.
- Evidence hint: New exact POST source for architecture and safety contracts; no offensive execution authorized.
- Matrix: `docs/intake/BRAIN_OS_POST_BATCH_INSIGHTS_MATRIX_2026-05-18.json`.

## Decision

`DOCUMENTED_FOR_SELECTIVE_EXTRACTION_ONLY`.

No source was moved, extracted into runtime, published or imported.
