import { useMemo, useState } from "react";
import type { TimeOfDay, WeatherMode } from "../pixelRealism/renderPasses";
import { VIBE_PRESETS } from "../vibecoding/vibePresets";
import type { PlayableLightKind, PlayableMaterial, PlayableSceneState, SceneInteractionTool } from "../scene/sceneTypes";

interface SceneInteractionPanelProps {
  scene: PlayableSceneState;
  tool: SceneInteractionTool;
  material: PlayableMaterial;
  lightKind: PlayableLightKind;
  onTool: (tool: SceneInteractionTool) => void;
  onMaterial: (material: PlayableMaterial) => void;
  onLightKind: (kind: PlayableLightKind) => void;
  onTogglePause: () => void;
  onStep: () => void;
  onTimeOfDay: (time: TimeOfDay) => void;
  onWeather: (weather: WeatherMode) => void;
  onApplyVibePreset: (preset: string) => void;
  onSaveScene: () => void;
  onLoadScene: (json: string) => void;
  onExportRpgScene: () => void;
  onRunPlayableQa?: () => void;
  qaSummary?: string;
}

const MATERIALS: PlayableMaterial[] = ["water", "fire", "smoke", "stone", "wood", "neon"];
const LIGHTS: PlayableLightKind[] = ["torch", "window", "neon", "fire", "magic", "signal", "ruin_anomaly"];
const TIMES: TimeOfDay[] = ["dawn", "day", "golden", "night", "interior"];
const WEATHER: WeatherMode[] = ["clear", "rain", "snow", "fog", "jungle_mist", "desert_haze"];

export function SceneInteractionPanel({
  scene,
  tool,
  material,
  lightKind,
  onTool,
  onMaterial,
  onLightKind,
  onTogglePause,
  onStep,
  onTimeOfDay,
  onWeather,
  onApplyVibePreset,
  onSaveScene,
  onLoadScene,
  onExportRpgScene,
  onRunPlayableQa,
  qaSummary,
}: SceneInteractionPanelProps) {
  const [vibePreset, setVibePreset] = useState(scene.activeVibe?.id ?? "neon_rain_street");
  const [loadText, setLoadText] = useState("");
  const summary = useMemo(() => [
    `${scene.metrics.activeMaterialCells} materials`,
    `${scene.metrics.activeLightSources} lights`,
    `${scene.metrics.particles} particles`,
    `${scene.timeOfDay}/${scene.weather}`,
  ].join(" · "), [scene]);

  return (
    <div className="section scene-panel">
      <div className="section-title">Playable Scene</div>
      <div className="scene-summary">{summary}</div>
      <div className="speed-row">
        {(["select", "city", "material", "light", "erase"] as SceneInteractionTool[]).map(item => (
          <button key={item} className={`speed-btn ${tool === item ? "active" : ""}`} onClick={() => onTool(item)}>
            {label(item)}
          </button>
        ))}
      </div>
      <div className="ctrl-row compact">
        <button className={`ctrl-btn ${!scene.paused ? "primary" : ""}`} onClick={onTogglePause}>
          {scene.paused ? "Play" : "Pause"}
        </button>
        <button className="ctrl-btn" onClick={onStep}>Step</button>
      </div>
      <label className="field-label">Material</label>
      <select className="select-input" value={material} onChange={event => onMaterial(event.target.value as PlayableMaterial)}>
        {MATERIALS.map(item => <option key={item} value={item}>{item}</option>)}
      </select>
      <label className="field-label">Light</label>
      <select className="select-input" value={lightKind} onChange={event => onLightKind(event.target.value as PlayableLightKind)}>
        {LIGHTS.map(item => <option key={item} value={item}>{item}</option>)}
      </select>
      <label className="field-label">Time</label>
      <select className="select-input" value={scene.timeOfDay} onChange={event => onTimeOfDay(event.target.value as TimeOfDay)}>
        {TIMES.map(item => <option key={item} value={item}>{item}</option>)}
      </select>
      <label className="field-label">Weather</label>
      <select className="select-input" value={scene.weather} onChange={event => onWeather(event.target.value as WeatherMode)}>
        {WEATHER.map(item => <option key={item} value={item}>{item}</option>)}
      </select>
      <label className="field-label">Vibe Preset</label>
      <select className="select-input" value={vibePreset} onChange={event => setVibePreset(event.target.value)}>
        {Object.keys(VIBE_PRESETS).map(id => <option key={id} value={id}>{id}</option>)}
      </select>
      <div className="ctrl-row compact">
        <button className="ctrl-btn" onClick={() => onApplyVibePreset(vibePreset)}>Apply Vibe</button>
      </div>
      <div className="ctrl-row compact">
        <button className="ctrl-btn" onClick={onSaveScene}>Save Scene</button>
        <button className="ctrl-btn" onClick={onExportRpgScene}>Export RPG</button>
      </div>
      <div className="ctrl-row compact">
        <button className="ctrl-btn" onClick={onRunPlayableQa}>Run QA Sequence</button>
      </div>
      {qaSummary && <div className="panel-note">{qaSummary}</div>}
      <textarea
        className="scene-json-input"
        placeholder="Paste scene JSON to load"
        value={loadText}
        onChange={event => setLoadText(event.target.value)}
      />
      <div className="ctrl-row compact">
        <button className="ctrl-btn" onClick={() => onLoadScene(loadText)} disabled={loadText.trim().length === 0}>Load Scene JSON</button>
      </div>
      <div className="panel-note">Click canvas with Material, Light or Erase selected. This is local deterministic scene state.</div>
    </div>
  );
}

function label(tool: SceneInteractionTool): string {
  if (tool === "select") return "Select";
  if (tool === "city") return "City";
  if (tool === "material") return "Material";
  if (tool === "light") return "Light";
  return "Erase";
}
