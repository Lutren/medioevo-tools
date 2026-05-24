# TEST_REPORT

## 2026-05-22 - Smallville-DUAT Evidence Refresh

StateFingerprint: SMALLVILLE-DUAT-LOCAL-EVIDENCE-20260522

### Comandos

```powershell
python -B -m pytest tests/test_smallville_duat_lab.py tests/test_smallville_duat_v02.py -q -p no:cacheprovider
python -B -m geodia_social_observatory.cli smallville-v02-report --seed 20260522 --ticks 12 --out-dir ..\..\qa_artifacts\smallville_duat\SMALLVILLE_DUAT_20260522 --out ..\..\qa_artifacts\smallville_duat\SMALLVILLE_DUAT_20260522\manifest.json --pretty
python -B -m geodia_social_observatory.cli smallville-duat --seed cierre-20260522 --days 1 --ticks-per-day 2 --pretty --out ..\..\qa_artifacts\smallville_duat\SMALLVILLE_DUAT_20260522\smallville_v01_ledger.json
python -B -m geodia_social_observatory.cli smallville-falsify --ledger ..\..\qa_artifacts\smallville_duat\SMALLVILLE_DUAT_20260522\smallville_v01_ledger.json --pretty --out ..\..\qa_artifacts\smallville_duat\SMALLVILLE_DUAT_20260522\smallville_v01_falsifier.json
python -B -m pytest tests -q -p no:cacheprovider
```

### Resultados

- Smallville focal v0.1/v0.2: `21 passed in 3.02s`.
- GEODIA full suite: `74 passed in 51.53s`.
- Metrics v0.2: `agents=25`, `hash_chain_valid=True`,
  `falsifiers_passed=True`, `publication_gate=BLOCK`, `failed=[]`.
- Falsifier v0.1: `passed=True`, `checks=7`.
- No remote compute, red, datos reales, sensores, push, deploy ni publicacion.

### Artefactos QA

- `qa_artifacts/smallville_duat/SMALLVILLE_DUAT_20260522/manifest.json`.
- `qa_artifacts/smallville_duat/SMALLVILLE_DUAT_20260522/duat-smallville-metrics-v0-2.json`.
- `qa_artifacts/smallville_duat/SMALLVILLE_DUAT_20260522/smallville_v01_ledger.json`.
- `qa_artifacts/smallville_duat/SMALLVILLE_DUAT_20260522/smallville_v01_falsifier.json`.

Fecha: 2026-05-17
StateFingerprint: DUAT-SMALLVILLE-SCI-SIM-v0-2-20260517

## Comandos

```powershell
python -m pytest tests\test_smallville_duat_v02.py -q
python -m geodia_social_observatory.cli smallville-v02-report --seed 20260517 --ticks 1440 --intervention weather_shock --pretty --out ..\..\qa_artifacts\release_validation\duat-smallville-v0-2-manifest.json
python -m pytest -q
python -m pytest -q
python -m compileall geodia_social_observatory
python -m geodia_social_observatory.cli smallville-replay-verify --pack ..\..\qa_artifacts\release_validation\duat-smallville-signal-pack-v0-2.json --ledger ..\..\qa_artifacts\release_validation\duat-smallville-baseline-run-v0-2-ledger.json --pretty --out ..\..\qa_artifacts\release_validation\duat-smallville-replay-verification-v0-2.json
python -m geodia_social_observatory.cli smallville-metrics --pack ..\..\qa_artifacts\release_validation\duat-smallville-signal-pack-v0-2.json --baseline ..\..\qa_artifacts\release_validation\duat-smallville-baseline-run-v0-2-ledger.json --intervention-run ..\..\qa_artifacts\release_validation\duat-smallville-intervention-run-v0-2-ledger.json --delta ..\..\qa_artifacts\release_validation\duat-smallville-intervention-delta-v0-2.json --pretty --out ..\..\qa_artifacts\release_validation\duat-smallville-metrics-v0-2.json
```

## Resultados

- GEODIA Smallville v0.2 focused: `14 passed`.
- GEODIA full suite: `74 passed`.
- DUAT predictive registry full suite: `117 passed`.
- Compileall: PASS.
- Schema validation artifacts: PASS.
- SecretScan focal presence-only: PASS.

## Artefactos QA

- `qa_artifacts/release_validation/duat-smallville-signal-pack-v0-2.json`
  - SHA256: `0B0BFD5A63130DD294C8BA126DD4258939DFE3741104BDEC1A78D9D14EA82F13`
  - uses_real_data: `false`
  - uses_network: `false`
  - publication_gate: `BLOCK`
- `qa_artifacts/release_validation/duat-smallville-baseline-run-v0-2-ledger.json`
  - SHA256: `7FC3F0802DE287DBE4AE4F8B110EF7688F647706DAE54C212D1F3EECEC785EAE`
  - agents: `25`
  - events: `1440`
- `qa_artifacts/release_validation/duat-smallville-intervention-run-v0-2-ledger.json`
  - SHA256: `4F2D3FD30BF8CB06608F027314D4660EA9C7C4B1785E73DCFD1E2C7ED88AD6B4`
- `qa_artifacts/release_validation/duat-smallville-metrics-v0-2.json`
  - SHA256: `6D0AFD4BA480A4D3D86029F5DAA66C18AC6D3B5E9122797F209219A2AB123DEC`
  - replay_verified: `true`
  - hash_chain_valid: `true`
  - falsifier pass_rate: `1.0`
  - failed: `[]`
- `qa_artifacts/release_validation/DUAT_SMALLVILLE_SIM_LAB_v0_2_REPORT.md`
  - SHA256: `DD00FA0686376A1CACDA289ECD9B55783CDA2B8AEB129F89BB8D6C848B0988A3`
