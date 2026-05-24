import { useMemo, useState } from "react";
import type { CityState, Mode } from "../core/types";
import type { ViewMode } from "../graphics/types";
import { createDefaultIsoRendererConfig, createIsoSceneAdapter } from "../iso3d/isoSceneAdapter";
import type { IsoLightProfile, IsoRendererMode } from "../iso3d/isoTypes";
import { applyVermeerIsoLighting, scoreVermeerIsoLegibility } from "../iso3d/vermeerIsoLighting";
import { RendererModeToggle, resolveRendererMode } from "./RendererModeToggle";

interface IsoRendererPanelProps {
  state: CityState;
  mode: Mode;
  viewMode: ViewMode;
}

export function IsoRendererPanel({ state, mode, viewMode }: IsoRendererPanelProps) {
  const [rendererMode, setRendererMode] = useState<IsoRendererMode>("canvas");
  const [populate, setPopulate] = useState(true);
  const [qOverlay, setQOverlay] = useState(viewMode === "DEBUG");
  const [heatmap, setHeatmap] = useState(viewMode !== "BEAUTIFUL");
  const [lightProfile, setLightProfile] = useState<IsoLightProfile>("vermeer");

  const modeState = resolveRendererMode(rendererMode, rendererMode === "iso3d");
  const scene = useMemo(() => {
    const base = createDefaultIsoRendererConfig(viewMode);
    const rawScene = createIsoSceneAdapter(state, {
      mode,
      viewMode,
      config: {
        ...base,
        enabled: modeState.isoEnabled,
        mode: rendererMode,
        populateBillboards: populate,
        qOverlay,
        heatmapOverlay: heatmap,
        lightProfile,
      },
    });
    return lightProfile === "vermeer" ? applyVermeerIsoLighting(rawScene) : rawScene;
  }, [heatmap, lightProfile, mode, modeState.isoEnabled, populate, qOverlay, rendererMode, state, viewMode]);
  const legibility = scoreVermeerIsoLegibility(scene);

  return (
    <div className="section" data-qa="iso-renderer-panel">
      <div className="section-title">Iso3D Renderer</div>
      <RendererModeToggle mode={rendererMode} onMode={setRendererMode} isoEnabled={modeState.isoEnabled} />
      <div className="speed-row">
        {(["vermeer", "caravaggio", "van_eyck", "medioevo"] as IsoLightProfile[]).map(profile => (
          <button key={profile} className={`speed-btn ${lightProfile === profile ? "active" : ""}`} onClick={() => setLightProfile(profile)}>
            {profile === "van_eyck" ? "van Eyck" : profile}
          </button>
        ))}
      </div>
      <div className="ctrl-row compact">
        <button className={`ctrl-btn ${populate ? "primary" : ""}`} onClick={() => setPopulate(!populate)}>Billboards</button>
        <button className={`ctrl-btn ${qOverlay ? "primary" : ""}`} onClick={() => setQOverlay(!qOverlay)}>Q Overlay</button>
      </div>
      <div className="ctrl-row compact">
        <button className={`ctrl-btn ${heatmap ? "primary" : ""}`} onClick={() => setHeatmap(!heatmap)}>Heatmap</button>
        <button className="ctrl-btn" onClick={() => { setRendererMode("canvas"); setLightProfile("vermeer"); }}>Reset Camera</button>
      </div>
      <div className="stat-row"><span className="stat-key">Mode</span><span className="stat-val">{scene.rendererMode}/{scene.mode}</span></div>
      <div className="stat-row"><span className="stat-key">Sprites</span><span className="stat-val">{scene.metrics.visibleSprites}</span></div>
      <div className="stat-row"><span className="stat-key">Draw calls</span><span className="stat-val">{scene.metrics.drawCallsEstimate}</span></div>
      <div className="stat-row"><span className="stat-key">Cache hit</span><span className="stat-val">{scene.metrics.cacheHitRatio.toFixed(2)}</span></div>
      <div className="stat-row"><span className="stat-key">Vermeer</span><span className="stat-val">{legibility.toFixed(2)}</span></div>
      <IsoMiniPreview scenePoints={scene.billboards.slice(0, 18).map(item => ({ id: item.id, x: item.position.x, y: item.position.y, color: item.tint }))} />
      <div className="panel-note">Feature-flagged adapter. No raw Lovable code runs; Canvas fallback remains available.</div>
    </div>
  );
}

function IsoMiniPreview({ scenePoints }: { scenePoints: Array<{ id: string; x: number; y: number; color: string }> }) {
  return (
    <div
      data-qa="iso-mini-preview"
      style={{
        position: "relative",
        height: 84,
        marginTop: 8,
        overflow: "hidden",
        border: "1px solid rgba(217, 199, 148, 0.25)",
        background: "linear-gradient(180deg, rgba(35,34,36,0.8), rgba(21,20,22,0.95))",
      }}
    >
      {scenePoints.map((point, index) => (
        <span
          key={point.id}
          title={point.id}
          style={{
            position: "absolute",
            left: `${48 + ((point.x + index * 7) % 96)}%`,
            top: `${18 + ((point.y + index * 11) % 54)}%`,
            width: 6,
            height: 10,
            imageRendering: "pixelated",
            background: point.color,
            boxShadow: "0 0 8px rgba(255, 219, 160, 0.22)",
            transform: "skewY(-18deg)",
          }}
        />
      ))}
    </div>
  );
}
