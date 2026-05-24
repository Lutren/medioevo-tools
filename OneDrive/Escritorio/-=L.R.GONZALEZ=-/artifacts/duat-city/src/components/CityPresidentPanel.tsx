import type { CityState } from "../core/types";

export function CityPresidentPanel({ state, onPolicy }: { state: CityState; onPolicy?: (policy: string, delta: number) => void }) {
  return (
    <div className="section">
      <div className="section-title">City President</div>
      <div className="stat-row"><span className="stat-key">Trust</span><span className="stat-val">{state.resources.trust.toFixed(1)}</span></div>
      <div className="stat-row"><span className="stat-key">Food</span><span className="stat-val">{state.resources.food.toFixed(1)}</span></div>
      <div className="ctrl-row">
        <button className="ctrl-btn" onClick={() => onPolicy?.("knowledge", 0.25)}>Knowledge</button>
        <button className="ctrl-btn" onClick={() => onPolicy?.("safety", 0.25)}>Safety</button>
      </div>
    </div>
  );
}
