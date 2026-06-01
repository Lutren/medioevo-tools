// DUAT Genesis Integration — Ported selectively from New project 3
// Provides: Float32Array field simulation, LG metrics, overlays, presets, sweep
// Not a game-play module: falsification laboratory for the DUAT field engine

export {
  DuatEngine,
  type DuatEngineParams,
  type DuatSeedMode,
} from "./engine";

export {
  MetricsTracker,
  computeBaseMetrics,
  computeRestrictionMatrixG,
  computeFisherL,
  computeLGModeSpectrum,
  computeDimObsAndAtum,
  classifyCosmology,
  type LGModeSpectrum,
  type SimulationMetrics,
} from "./metrics";

export {
  renderPsiOverlay,
  renderGravityOverlay,
  renderLightOverlay,
  renderObserverDeltaOverlay,
  type OverlayKind,
} from "./overlays";

export {
  FERTILE_PRESETS,
  INFERTILE_PRESETS,
  PLAYABLE_PRESET,
  type PresetConfig,
} from "./presets";

export {
  runDuatSweep,
  summarizeSweep,
  buildPhaseMap,
  sweepRowsToCsv,
  sweepSummaryToMarkdown,
  sweepPhaseMapToMarkdown,
  type SweepConfig,
  type SweepRow,
  type SweepSummary,
  type PhaseMapCell,
} from "./sweep";
