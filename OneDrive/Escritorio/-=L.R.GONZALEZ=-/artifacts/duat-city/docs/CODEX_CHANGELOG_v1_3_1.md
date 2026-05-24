# CODEX CHANGELOG v1.3.1

Fingerprint: DUAT-v1.3.1-AUDIO-GAMEFEEL-CONTINUITY

## Added

- Deterministic local audio/game-feel adapter.
- Browser WebAudio procedural synth, disabled until user gesture.
- Audio/Game Feel toolbar panel.
- Agent Life relationship graph and dashboard.
- Audio integration in GameState, BrainRuntime, Handoff and RPG export v3.
- Audio/game-feel benchmark runner.
- Screenshot capture script for v1.3.1.
- Audio, agent and asset game-feel manifests.

## Changed

- Handoff now includes `audio_gamefeel`.
- BrainRuntime now exposes `audioGameFeel`.
- RPG world export now includes `audio_gamefeel_profile`.
- Pixel game-feel budget caps cue and pulse pressure by quality preset.

## Fixed

- Clamped procedural synth jitter after frequency normalization.
- Avoided storing a field name containing `NaN` inside GameState JSON so the existing no-NaN regression remains meaningful.

## Boundary

- No copied assets.
- No external samples.
- No cloud/API.
- No push/deploy/commit.
- Wabi execution remains disabled.
