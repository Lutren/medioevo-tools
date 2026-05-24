# ASSUMPTIONS v1.1

Fingerprint: DUAT-v1.1-PLAYABLE-SCENE-QA

- The correct v1.1 scope is local playable usability and QA evidence, not new theory or asset import.
- `artifacts/duat-city` is the allowed work target for this cycle.
- Screenshots under `docs/screenshots/v1_1/` are QA artifacts, not production assets.
- The existing dev server on `127.0.0.1:18519` can be reused if it serves `/duat-city/` with HTTP 200.
- Local `127.0.0.1` CDP and HTTP smoke are permitted local QA actions and do not violate the no-cloud/API boundary.
- Wabi must remain disabled even if v1.1 adds authoring controls.
