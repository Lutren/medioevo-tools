import type { CityState } from "../core/types";

interface MaterialPanelProps {
  state: CityState;
}

export function MaterialPanel({ state }: MaterialPanelProps) {
  const hazards = state.fieldSummary?.hazards ?? [];
  return (
    <div className="mini-panel">
      <div className="stat-row"><span className="stat-key">Material cells</span><span className="stat-val">{state.fieldMetrics?.activeCells ?? 0}</span></div>
      <div className="stat-row"><span className="stat-key">Field R</span><span className="stat-val">{(state.fieldMetrics?.R_field ?? 0).toFixed(3)}</span></div>
      <div className="stat-row"><span className="stat-key">Water</span><span className="stat-val">{state.tiles.filter(t => t.type === "water").length}</span></div>
      <div className="stat-row"><span className="stat-key">Ruins</span><span className="stat-val">{state.buildings.filter(b => b.type === "ruin").length}</span></div>
      {hazards.length > 0 && <div className="panel-note">{hazards.slice(0, 3).join(", ")}</div>}
    </div>
  );
}
