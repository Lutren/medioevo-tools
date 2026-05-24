# RISKS v1.1

Fingerprint: DUAT-v1.1-PLAYABLE-SCENE-QA

- Automated visible Edge benchmark appears focus/throttling limited. The harness is real and finite, but the numbers should not be treated as final user-facing FPS.
- HIGH/BEAUTIFUL scenarios currently activate up to 57,600 light cells; optimization is needed before claiming stable high-end performance.
- Visual quality is procedural and improved for QA, but production quality still depends on reviewed/allowlisted assets.
- Pixel/cell physics intentionally uses simple approximations. It supports gameplay feedback, not exact fluid, heat, smoke or optics simulation.
- Scene save/load is local JSON only; long-term compatibility will need schema version migrations if the scene model changes.
