# RISKS ENGINE EXTENSIONS 2026-05-22

- Parent workspace is broadly dirty/untracked; do not use broad staging, reset, cleanup, or movement.
- Private Godot RPG passed validators, but it remains private and not publishable.
- `MEDIOEVO_RPG_ENGINE_EXPORT_v2.md` now documents current v3 export truth, but the filename remains v2 for historical continuity.
- The dev server requires `PORT` and `BASE_PATH`; start with `PORT=5175` and `BASE_PATH=/` for local smoke.
- Story bible validator reports `STORY_BIBLE_COMPLETION_BLOCKED_OK TODO=245`; keep this as content work, not engine failure.
- Browser visual QA depends on local Microsoft Edge/CDP availability; it is evidence for the current machine, not a cross-browser certification.
- The fixed compact layout was validated at 390x844 and desktop 1366x900; additional viewport sweeps can be added later if the UI grows.
