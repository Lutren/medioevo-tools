import type { CityState } from "../core/types";
import { ResourcePanel } from "./ResourcePanel";
import { rColor, GATE_COLORS } from "../render/palette";

interface CityPanelProps {
  state: CityState;
  selectedId: string | null;
  onSelect: (id: string | null) => void;
  showHeatmap: boolean;
  onShowHeatmap: (v: boolean) => void;
  showFibmob: boolean;
  onShowFibmob: (v: boolean) => void;
  showAgentLabels: boolean;
  onShowAgentLabels: (v: boolean) => void;
  onResetCamera: () => void;
}

export function CityPanel({
  state, selectedId, onSelect,
  showHeatmap, onShowHeatmap,
  showFibmob, onShowFibmob,
  showAgentLabels, onShowAgentLabels,
  onResetCamera,
}: CityPanelProps) {
  const { buildings, agents, R, Phi_eff } = state;

  return (
    <div className="panel-right">
      <div className="section">
        <div className="section-title">City Metrics</div>
        <div className="stat-row">
          <span className="stat-key">Global R</span>
          <span className="stat-val" style={{ color: rColor(R) }}>{R.toFixed(3)}</span>
        </div>
        <div className="need-row" style={{ marginBottom: 3 }}>
          <div className="need-bar-wrap">
            <div className="progress-bar"><div className="progress-fill bar-r" style={{ width: `${R * 100}%` }} /></div>
          </div>
        </div>
        <div className="stat-row">
          <span className="stat-key">Φ_eff</span>
          <span className="stat-val" style={{ color: rColor(1 - Phi_eff) }}>{Phi_eff.toFixed(3)}</span>
        </div>
        <div className="need-row" style={{ marginBottom: 3 }}>
          <div className="need-bar-wrap">
            <div className="progress-bar"><div className="progress-fill bar-phi" style={{ width: `${Phi_eff * 100}%` }} /></div>
          </div>
        </div>
        <div className="stat-row">
          <span className="stat-key">Buildings</span>
          <span className="stat-val">{buildings.length}</span>
        </div>
        <div className="stat-row">
          <span className="stat-key">Tasks pending</span>
          <span className="stat-val">{state.tasks.filter(t => t.status === "active").length}</span>
        </div>
      </div>

      <div className="section">
        <div className="section-title">View</div>
        <div className="ctrl-row">
          <button className={`ctrl-btn ${showHeatmap ? "primary" : ""}`} onClick={() => onShowHeatmap(!showHeatmap)}>R Heatmap</button>
          <button className={`ctrl-btn ${showFibmob ? "primary" : ""}`} onClick={() => onShowFibmob(!showFibmob)}>FibMob</button>
        </div>
        <div className="ctrl-row">
          <button className={`ctrl-btn ${showAgentLabels ? "primary" : ""}`} onClick={() => onShowAgentLabels(!showAgentLabels)}>Labels</button>
          <button className="ctrl-btn" onClick={onResetCamera}>⌂ Center</button>
        </div>
      </div>

      <ResourcePanel state={state} />

      <div className="section">
        <div className="section-title">Buildings</div>
        {buildings.length === 0 && <div className="stat-key">No buildings yet</div>}
        {buildings.slice(-8).reverse().map(b => (
          <div
            key={b.id}
            className={`agent-item ${selectedId === b.id ? "selected" : ""}`}
            onClick={() => onSelect(b.id)}
          >
            <span className="agent-name">{b.name}</span>
            <span className="agent-gate-tag" style={{ background: `${GATE_COLORS[b.gate]}22`, color: GATE_COLORS[b.gate] }}>
              {b.gate.slice(0, 3)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
