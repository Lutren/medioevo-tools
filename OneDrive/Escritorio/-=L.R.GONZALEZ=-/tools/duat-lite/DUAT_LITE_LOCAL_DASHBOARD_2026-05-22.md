# DUAT Lite Local Dashboard - 2026-05-22

## Estado

Dashboard local implementado en `tools/duat-lite`.

## Superficie

- `server.py`: servidor HTTP stdlib.
- `index.html`: dashboard responsive.
- `tests/test_duat_lite_server.py`: smoke HTTP.

## Paneles

- Claim intake.
- Gate.
- R.
- Phi_eff.
- Claims activos.
- Next action.
- ObservationEnvelope JSON.

## Evidencia

- `python -B -m pytest tools/duat-lite/tests -q -p no:cacheprovider`
  -> `1 passed in 0.97s`.
- `python -B -m py_compile tools/duat-lite/server.py tools/duat-lite/tests/test_duat_lite_server.py`
  -> PASS.
- HTTP smoke efimero:
  - page 200, title present.
  - `/api/health` 200 `ok`.
  - `/api/classify` 200, `claim_count=1`, `gate=APPROVE`,
    `publication_gate=BLOCK`, `cloud_provider_called=false`.
- Visual QA:
  - `qa_artifacts/ui_visual_qa/DUAT_LITE_20260522/duat_lite_dashboard_1366x900.png`
  - `qa_artifacts/ui_visual_qa/DUAT_LITE_20260522/duat_lite_dashboard_390x844.png`

## Gates

- `publication_gate=BLOCK`.
- No cloud/provider call.
- No source apply.
- No dependency install.
- Server used only as temporary local QA and was stopped after screenshots.
