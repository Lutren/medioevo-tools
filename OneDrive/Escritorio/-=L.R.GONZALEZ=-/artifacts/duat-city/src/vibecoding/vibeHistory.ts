import type { PixelRealismConfig } from "../pixelRealism/renderPasses";
import type { PlayableSceneState } from "../scene/sceneTypes";
import type { VibeSceneConfig } from "./vibeTypes";

export interface VibeUndoSnapshot {
  activeVibeScene?: VibeSceneConfig;
  visualConfig: PixelRealismConfig;
  playableScene: PlayableSceneState;
}

export function createVibeUndoSnapshot(
  activeVibeScene: VibeSceneConfig | undefined,
  visualConfig: PixelRealismConfig,
  playableScene: PlayableSceneState,
): VibeUndoSnapshot {
  return {
    activeVibeScene,
    visualConfig: { ...visualConfig },
    playableScene: {
      ...playableScene,
      materials: playableScene.materials.map(cell => ({ ...cell })),
      lights: playableScene.lights.map(light => ({ ...light })),
      metrics: { ...playableScene.metrics, qStateCounts: { ...playableScene.metrics.qStateCounts } },
    },
  };
}

export function restoreVibeUndoSnapshot(snapshot: VibeUndoSnapshot): VibeUndoSnapshot {
  return createVibeUndoSnapshot(snapshot.activeVibeScene, snapshot.visualConfig, snapshot.playableScene);
}
