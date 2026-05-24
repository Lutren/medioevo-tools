import type { CityState } from "../core/types";
import { createHormigueroHeatmap } from "../gameModes/hormigueroMode";

export function HormigueroPanel({ state }: { state: CityState }) {
  const heatmap = createHormigueroHeatmap(state);
  const highR = heatmap.filter(cell => cell.R > 0.45).length;
  return (
    <div className="section">
      <div className="section-title">Hormiguero</div>
      <div className="stat-row"><span className="stat-key">Control</span><span className="stat-val">observer only</span></div>
      <div className="stat-row"><span className="stat-key">Cells</span><span className="stat-val">{heatmap.length}</span></div>
      <div className="stat-row"><span className="stat-key">High R</span><span className="stat-val">{highR}</span></div>
    </div>
  );
}
