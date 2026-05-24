import type { CityState } from "../core/types";
import type { PixelRealismConfig } from "../pixelRealism/renderPasses";

interface PixelEnginePanelProps {
  state: CityState;
  config: PixelRealismConfig;
}

export function PixelEnginePanel({ state, config }: PixelEnginePanelProps) {
  return (
    <div className="section">
      <div className="section-title">Pixel Game Engine</div>
      <div className="scene-preview">
        <div><b>Quality:</b> {config.qualityPreset}</div>
        <div><b>Light R/Phi:</b> {(state.pixelRealism?.R_light ?? 0).toFixed(3)} / {(state.pixelRealism?.Phi_light ?? 1).toFixed(3)}</div>
        <div><b>Material cells:</b> {state.playableScene?.metrics.activeMaterialCells ?? 0}</div>
        <div><b>Light cells:</b> {state.pixelRealism?.activeLightCells ?? 0}</div>
        <div><b>Cache:</b> static terrain/building/postprocess dirty-key ready</div>
      </div>
    </div>
  );
}
