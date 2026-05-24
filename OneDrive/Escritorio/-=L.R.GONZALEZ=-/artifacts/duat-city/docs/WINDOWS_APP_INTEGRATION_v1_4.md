# DUAT Windows App Integration v1.4

Fingerprint: DUAT-v1.4-WINAPP-CONVERSION

## Runtime

DUAT v1.4 now has a local Windows executable path:

- `dist/winapp/DUATCity.exe`
- `dist/winapp/DUATCity-Launch.cmd`
- `dist/winapp/app/`
- `dist/winapp/WINAPP_MANIFEST_v1_4.json`

Electron/Tauri remain the preferred long-term wrappers, but neither dependency is present in the local project and installing them would require a dependency/network review. This pass uses a no-new-dependency native .NET Framework launcher that serves the built app from loopback and opens Microsoft Edge in App Mode.

## Preserved Features

- Iso3D renderer toggle.
- Canvas fallback.
- Pixel/Light Engine.
- Vermeer light profile.
- 2D pixel billboards.
- Audio/Game-Feel procedural panel with manual Enable/Preview.
- Agent Life, BrainRuntime, GameState and RPG export.
- OSIT formula profile, ScienceClaimGate and Observacionismo source manifest.

## Boundary

- `publication_allowed=false`
- `wabi_execution_allowed=false`
- `sandbox_execution_allowed=false`
- `real_apply_allowed=false`
- `cloud_used=false`
- `mcp_execution=false`
- `unknown_zip_code_executed=false`
- no new public assets copied

## QA Result

- Native launcher smoke: PASS.
- Loopback HTTP from `DUATCity.exe`: 200.
- JS asset smoke: 200.
- Audio/Game-Feel procedural preview: PASS by CDP fallback, 6 cues.
- Human audible audio: not verified.
- Winapp screenshot: first city overview captured; later CDP scene navigation timed out.
- Winapp benchmark fallback: Beautiful and Debug above 30 FPS; High/Operational below 30 FPS in this shell.

## Known Limitations

The generated executable is a local wrapper, not a signed installer. It does not bundle Electron/Tauri and it does not publish assets. True native headed FPS and human-audible audio still require manual owner QA on the local machine.
