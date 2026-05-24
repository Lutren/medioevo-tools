# Renderer Performance v1.3.2

Implementation focus:
- separate static terrain/building layers from dynamic agent layers;
- cache heatmap/Q glyph overlays independently;
- keep Canvas fallback active;
- cap visible billboards by view mode;
- keep light updates budgeted through scene metrics.

Measured QA:
- tests: 100 files / 303 tests PASS
- typecheck: PASS
- build: PASS
- HTTP smoke: 200
- screenshot capture: 10 PNGs generated via Edge/CDP headless

Current limitation:
- this pass did not add a new FPS benchmark JSON; the adapter exposes finite cost estimates and cache-hit metrics for follow-up headed FPS measurement.
