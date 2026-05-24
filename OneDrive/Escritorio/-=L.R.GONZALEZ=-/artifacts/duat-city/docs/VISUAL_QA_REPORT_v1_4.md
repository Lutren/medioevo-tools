# Visual QA Report v1.4

Screenshot QA completed through Edge/CDP headless.

Screenshots:
- `docs/screenshots/v1_4/full_integration_city_overview.png`
- `docs/screenshots/v1_4/osit_formula_lab_panel.png`
- `docs/screenshots/v1_4/audio_iso3d_game_os_panel.png`

Also inspected owner-provided screenshot:
- `Screenshot 2026-05-20 020022.png`

Visual finding:
- The owner screenshot points toward a full isometric game shell with compact diegetic chrome.
- Current DUAT v1.4 now has the relevant systems exposed, but the Iso3D renderer remains a typed adapter/preview rather than a full Lovable-style 3D scene renderer.
- Static render fallback benchmark now reaches >30 FPS for High playfield, Beautiful and Debug scenarios in Edge/CDP headless sampling.
- True headed FPS remains unconfirmed because the headed runner timed out in this local automation environment.

Next visual step:
- Graduate the Iso3D adapter into the main playfield renderer after dependency/license review.
