import type { IsoRendererMode } from "../iso3d/isoTypes";

export interface RendererModeState {
  requestedMode: IsoRendererMode;
  isoEnabled: boolean;
  canvasFallback: boolean;
  reason: string;
}

export function resolveRendererMode(requestedMode: IsoRendererMode, enableIso3d: boolean): RendererModeState {
  const isoEnabled = requestedMode === "iso3d" && enableIso3d;
  return {
    requestedMode,
    isoEnabled,
    canvasFallback: !isoEnabled,
    reason: isoEnabled
      ? "Iso3D adapter active with Canvas fallback preserved."
      : "Canvas renderer remains authoritative; Iso3D can be previewed by feature flag.",
  };
}

interface RendererModeToggleProps {
  mode: IsoRendererMode;
  onMode: (mode: IsoRendererMode) => void;
  isoEnabled: boolean;
}

export function RendererModeToggle({ mode, onMode, isoEnabled }: RendererModeToggleProps) {
  const state = resolveRendererMode(mode, isoEnabled);
  return (
    <>
      <div className="speed-row" data-qa="renderer-mode-toggle">
        {(["canvas", "iso3d"] as IsoRendererMode[]).map(value => (
          <button key={value} className={`speed-btn ${mode === value ? "active" : ""}`} onClick={() => onMode(value)}>
            {value === "canvas" ? "Canvas" : "Iso3D"}
          </button>
        ))}
      </div>
      <div className="panel-note">{state.reason}</div>
    </>
  );
}
