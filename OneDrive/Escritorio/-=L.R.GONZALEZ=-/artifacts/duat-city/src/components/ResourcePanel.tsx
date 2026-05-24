import type { CityState } from "../core/types";
import { ALL_RESOURCES, RESOURCE_LABELS, RESOURCE_ICONS, RESOURCE_MAX } from "../sim/resources";

interface ResourcePanelProps {
  state: CityState;
}

const BAR_CLASS: Record<string, string> = {
  food: "bar-food", materials: "bar-materials", knowledge: "bar-knowledge",
  trust: "bar-trust", signal: "bar-signal", energy: "bar-energyres", culture: "bar-culture",
};

export function ResourcePanel({ state }: ResourcePanelProps) {
  return (
    <div className="section">
      <div className="section-title">Resources</div>
      {ALL_RESOURCES.map(key => {
        const val = state.resources[key] ?? 0;
        const max = RESOURCE_MAX[key];
        const pct = (val / max) * 100;
        return (
          <div key={key} className="need-row">
            <span className="need-label">{RESOURCE_ICONS[key]} {RESOURCE_LABELS[key]}</span>
            <div className="need-bar-wrap">
              <div className="progress-bar">
                <div
                  className={`progress-fill ${BAR_CLASS[key]}`}
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
            <span className="stat-val" style={{ minWidth: 28, textAlign: "right", color: val < 20 ? "#ff4444" : "#c9d1d9" }}>
              {Math.round(val)}
            </span>
          </div>
        );
      })}
    </div>
  );
}
