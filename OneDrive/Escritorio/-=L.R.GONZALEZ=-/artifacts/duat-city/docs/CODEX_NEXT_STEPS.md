# DUAT Agent City — Codex Next Steps

## v0.9 Immediate Next Step

1. Approve a second narrow asset allowlist focused on buildings, tiles and agent sprites.
2. Replace the weakest procedural building silhouettes while keeping fallback rendering.
3. Improve agent activity glyphs for eat/rest/work/social without adding a new simulation system.
4. Create a MEDIOEVO living-city demo scenario with fixed camera presets and screenshot script.
5. Keep Wabi MCP workpacks design-only; do not enable execution.

## v0.8 Closed

- In-app FPS sampler added.
- OSIT Performance panel added.
- Camera framing presets added.
- Beautiful mode hardened for capture with minimal UI.
- Pixel/FibMob/debug overlays isolated outside Beautiful.

## Priority 1: Gameplay Depth

### 1.1 Building Upgrades
- Level system (1→2→3) for each building type
- Level 2: +50% production, -10% R_delta, requires materials
- Level 3: unique bonus (e.g., archive L3 generates daily handoff)
- UI: click building → show Upgrade button in BuildingInspector

### 1.2 Agent Pathfinding
- Replace linear lerp with simple A* on the tile grid
- Obstacles: buildings block movement (agents go around)
- Roads: 1.5x speed bonus when traversing road tiles
- Would make city layout matter (road networks)

### 1.3 Event Resolution
- Events should be interactive: "Accept" or "Dismiss" buttons
- Accepted events trigger task chains
- Dismissed events have negative R consequences

## Priority 2: RPG Integration

### 2.1 Import RPG JSON Back
- Allow importing a generated RPG world JSON to update the city
- Quest completions should modify resources/R
- Encounter outcomes should be playable in the city view

### 2.2 Faction Influence Map
- Color-code tiles by controlling faction
- Faction territory expands when they control more buildings
- Faction conflict generates REVIEW events

### 2.3 NPC Dialogue Export
- Generate dialogue trees for each NPC based on needs/memory
- Export as JSON compatible with RPG Maker / Godot / Unity

## Priority 3: OSIT Depth

### 3.1 R History Chart
- Plot R and Φ_eff over last 200 ticks
- Use recharts (already installed in the scaffold)
- Show regime transitions as colored bands

### 3.2 Witness Log Export
- Export full witness log as CSV or JSON
- Include evidence strings per entry

### 3.3 FibMob Lab Bridge
- Load duat-fibmob-lab handoff JSON into city
- Map lab R/Φ_eff → city starting state modifier
- Close the DUAT research loop

## Priority 4: Polish

### 4.1 Sound (optional)
- Use Web Audio API for ambient city sounds
- Building click sound, task completion chime, BLOCK alert

### 4.2 Tutorial Overlay
- First-run tooltip sequence
- Highlight key UI elements on first open

### 4.3 Mobile / Touch Support
- Pinch-to-zoom on canvas
- Touch-friendly button sizes

## Formal Lab Boundary
Per DUAT protocol: all FibMob arithmetic is computational only.
No physical, magnetic, or causal claims. The city is a formal model.
