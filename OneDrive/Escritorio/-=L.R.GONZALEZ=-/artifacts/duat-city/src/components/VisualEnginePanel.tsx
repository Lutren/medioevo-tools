import type { CityState } from "../core/types";
import type { PixelRealismConfig, RenderQualityPreset, TimeOfDay, WeatherMode } from "../pixelRealism/renderPasses";
import { LightPanel } from "./LightPanel";
import { MaterialPanel } from "./MaterialPanel";

interface VisualEnginePanelProps {
  state: CityState;
  config: PixelRealismConfig;
  onConfig: (config: PixelRealismConfig) => void;
}

export function VisualEnginePanel({ state, config, onConfig }: VisualEnginePanelProps) {
  return (
    <div className="section visual-engine-panel">
      <div className="section-title">Medioevo Pixel Realism</div>
      <label className="field-label">Quality</label>
      <select className="select-input" value={config.qualityPreset} onChange={event => onConfig({ ...config, qualityPreset: event.target.value as RenderQualityPreset })}>
        {(["LOW", "MEDIUM", "HIGH", "BEAUTIFUL", "DEBUG"] as RenderQualityPreset[]).map(value => <option key={value} value={value}>{value}</option>)}
      </select>
      <label className="field-label">Time</label>
      <select className="select-input" value={config.timeOfDay} onChange={event => onConfig({ ...config, timeOfDay: event.target.value as TimeOfDay })}>
        {(["dawn", "day", "golden", "night", "interior"] as TimeOfDay[]).map(value => <option key={value} value={value}>{value}</option>)}
      </select>
      <label className="field-label">Weather</label>
      <select className="select-input" value={config.weather} onChange={event => onConfig({ ...config, weather: event.target.value as WeatherMode })}>
        {(["clear", "rain", "snow", "fog", "jungle_mist", "desert_haze"] as WeatherMode[]).map(value => <option key={value} value={value}>{value}</option>)}
      </select>
      <label className="field-label">Palette</label>
      <select className="select-input" value={config.paletteProfile} onChange={event => onConfig({ ...config, paletteProfile: event.target.value })}>
        {["medioevo_archeopunk", "cinematic_teal_amber", "warm_interior", "pictorial_nature", "winter_reflection"].map(value => <option key={value} value={value}>{value}</option>)}
      </select>
      <div className="toggle-row">
        <label><input type="checkbox" checked={config.dither} onChange={event => onConfig({ ...config, dither: event.target.checked })} /> Dither</label>
        <label><input type="checkbox" checked={config.hideUiForCapture} onChange={event => onConfig({ ...config, hideUiForCapture: event.target.checked })} /> Capture</label>
      </div>
      <div className="stat-row">
        <span className="stat-key">Pixel scale</span>
        <span className="stat-val">{config.pixelScale}</span>
      </div>
      <input
        className="range-input"
        type="range"
        min="1"
        max="5"
        step="1"
        value={config.pixelScale}
        onChange={event => onConfig({ ...config, pixelScale: Number(event.target.value) })}
      />
      <LightPanel config={config} onConfig={onConfig} />
      <MaterialPanel state={state} />
    </div>
  );
}
