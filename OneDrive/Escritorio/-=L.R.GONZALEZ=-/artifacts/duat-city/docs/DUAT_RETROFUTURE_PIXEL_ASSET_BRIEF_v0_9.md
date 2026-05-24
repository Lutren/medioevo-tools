# DUAT RETROFUTURE PIXEL ASSET BRIEF v0.9

## Direction

DUAT City should look like a cinematic isometric 2D pixel-art simulation: retrofuturistic, archeopunk, steampunk, cyberpunk, ecopunk and solarpunk. The visual language can be inspired by cinematic neon pixel-art games, but must not copy characters, sprites, scenes, logos or layouts from any existing game.

The city is not a generic skin. The aesthetic must emerge from the physics and diagnostics: light, vapor, rain, dust, water, residue, signal, stone, copper, glass, CRT glow, solar panels, vines, ruins and agents must all communicate simulation state.

## Technical Constraints

- PNG sprites, transparent or removable chroma-key background.
- Pixel-perfect crisp edges; no soft blur, no watermark, no text.
- Isometric 2D / 2.5D, readable at small sizes.
- Runtime keeps procedural fallbacks.
- Generated assets must enter review first, with provenance and hash.
- `publication_allowed=false` until owner review.

## P0 Asset List

Tiles:

- `tile-road-archeopunk`
- `tile-plaza-bronze`
- `tile-water-neon-reflection`
- `tile-forest-solarpunk`
- `tile-stone-ancient`
- `tile-wall-industrial`
- `tile-empty-night-grid`

Buildings:

- `building-residential-stack`
- `building-workshop-steam`
- `building-market-neon`
- `building-archive-observatory`
- `building-clinic-biolight`
- `building-ruin-anomaly`
- `building-gatehouse-signal`

Agents:

- `agent-observer`
- `agent-archivist`
- `agent-worker`
- `agent-courier`
- `agent-storykeeper`

Physics materials/effects:

- water falling/settled;
- smoke rising;
- fire burning and emitting light;
- dust falling;
- light pulse;
- residue/anomaly particle;
- missing signal marker.

UI/OSIT:

- Q-state glyphs `00`, `01`, `10`, `11`;
- R/Phi meters;
- ActionGate icons APPROVE/REVIEW/BLOCK;
- WitnessLog and Handoff icons;
- Quaternary timing panel frame.

## Prompt Template

```text
Create a pixel-perfect isometric 2D game asset for DUAT City.

Subject:
[asset name]

Visual identity:
retrofuturistic archeopunk city, cinematic neon pixel art, steampunk machinery, cyberpunk wet light, ecopunk/solarpunk overgrowth, ancient stone plus copper circuitry, dark night atmosphere with controlled cyan/amber/magenta highlights.

Camera and format:
isometric 2D sprite, transparent background or flat #00ff00 chroma-key background, crisp pixel edges, no soft blur, no text, no logo, no watermark.

Technical constraints:
must read clearly at small size, compatible with tile-based city builder, no copied game assets, no direct imitation of any existing game scene or character.

State variant:
[clean / active / damaged review / blocked anomaly]

Physics meaning:
material behavior should imply [water falls / smoke rises / fire emits light / stone is stable / signal is missing / agent is moving / residue is unstable].
```

