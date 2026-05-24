# ART_DIRECTION_CANON_v1_2

Fingerprint: DUAT-v1.2-ASSET-AWARE-PIXEL-GAME-ENGINE

## Scope

This canon adds internal MEDIOEVO art-direction tokens to DUAT. It uses visual principles only: dramatic lateral contrast, calm interior light, micro material detail, symbolic composition, wet reflection, fog and diegetic UI.

Boundary: no copied protected scenes, characters, worlds or text. Historical artist names are internal authoring handles only and are not public marketing claims.

## Light Canon

- `caravaggio_chiaroscuro` -> `high_contrast_revelation`: high contrast, deep shadow, lateral light for danger, revelation, gates, judgement and ruins.
- `vermeer_interior_light` -> `soft_interior_window_light`: controlled side-window softness for taverns, archives, workshops, memory and conversation.
- `van_eyck_detail_light` -> `micro_material_detail`: reflective metal/glass/water and readable props, relics, UI and inventory.
- `balanced_medioevo` -> `balanced_medioevo_cinematic_light`: default readable MEDIOEVO cinematic profile.

Implemented in `src/artDirection/lightCanon.ts`.

## Material Detail Canon

Prioritized materials include aged brass, burnished copper, obsidian glass, wet stone, patinated bronze, bioluminescent algae, ritual amber, smoked crystal, carbonized wood, moss/organic membrane, rain-wet metal and old paper/archive tablet.

Implemented in `src/artDirection/materialDetailCanon.ts`.

## Composition

Scenes use foreground frames, midground action, background depth, light path, 13 symbolic objects and hierarchy budgets so not every surface is saturated equally.

Implemented in `src/artDirection/compositionCanon.ts` and `src/artDirection/symbolicObjectGrammar.ts`.
