import type { PixelRealismConfig } from "../pixelRealism/renderPasses";

interface LightPanelProps {
  config: PixelRealismConfig;
  onConfig: (config: PixelRealismConfig) => void;
}

export function LightPanel({ config, onConfig }: LightPanelProps) {
  return (
    <div className="mini-panel">
      <div className="stat-row">
        <span className="stat-key">Intensity</span>
        <span className="stat-val">{config.lightIntensity.toFixed(2)}</span>
      </div>
      <input
        className="range-input"
        type="range"
        min="0.4"
        max="1.8"
        step="0.05"
        value={config.lightIntensity}
        onChange={event => onConfig({ ...config, lightIntensity: Number(event.target.value) })}
      />
      <div className="stat-row">
        <span className="stat-key">Bloom</span>
        <span className="stat-val">{config.bloomAmount.toFixed(2)}</span>
      </div>
      <input
        className="range-input"
        type="range"
        min="0"
        max="0.8"
        step="0.04"
        value={config.bloomAmount}
        onChange={event => onConfig({ ...config, bloomAmount: Number(event.target.value) })}
      />
    </div>
  );
}
