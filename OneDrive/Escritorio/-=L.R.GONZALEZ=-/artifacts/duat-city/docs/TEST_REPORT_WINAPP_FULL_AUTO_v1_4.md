# Test Report Windows App v1.4 Full Auto

Fingerprint: DUAT-v1.4-WINAPP-FULL-AUTO
Generated: 2026-05-20T12:40:11.2525693Z
Run dir: $run

## Results

- Unit/integration/regression: PASS, 106 files / 313 tests.
- Typecheck: PASS.
- Web build: PASS.
- Windows app build: PASS.
- Windows app smoke: PASS, HTTP 200, JS asset 200.
- Windows benchmark: PASS, min app avg FPS 60.17, threshold 30.
- Audio/Game-Feel: PASS for browser AudioContext, local gesture, and procedural preview; headed focus focused; preview $(@{schema=duat/audio-headed-qa/v1.4; fingerprint=DUAT-v1.4-OSIT-OBSERVACIONISMO-FULL; generatedAt=05/20/2026 12:22:00; appUrl=http://127.0.0.1:18651/duat-city/?mode=CITY&view=OPERATIONAL&sceneDemo=fire_smoke&vibe=warm_interior_tavern&nativeWin=1; browserMode=Edge/CDP/headed; focusAttempt=focused_by_pid; focusStatus=focused; audioOffByDefault=True; browserAudioAvailable=True; enableClicked=True; previewClicked=True; afterEnable=; afterPreview=; enableLatencyMs=64603.5; previewLatencyMs=60744.9; proceduralPreviewConfirmed=True; audibleConfirmedByHuman=False; notes=System.Object[]}.afterPreview.lastPreview); cue count 22.
- Screenshots: PASS, 8 PNGs, all nonblank: True.
- Asset integrity: PASS, 21 asset manifests parse, 8 reviewed assets hash-match, active zip count 0.

## Corrections Applied

- Memoized LOD, graphics budget and graphics metrics in src/App.tsx.
- Stabilized onRenderCounters so FPS sampler state updates do not force canvas redraws.
- Added 	ools/run-winapp-benchmark-v1_4.mjs and moved winapp:benchmark:headed to the manual headed runner.
- Expanded 	ools/capture-screenshots-v1_4.mjs to cover Canvas, Iso3D, billboards, Q/debug overlay, Audio/Game-Feel, Agent Life and Vermeer panels.

## Boundary

- No push, deploy, commit, cloud, MCP or Wabi execution.
- No unknown zip executed.
- Publication remains false.
- Audio human audibility is not claimed; the verified state is browser audio availability plus local gesture plus procedural preview.
