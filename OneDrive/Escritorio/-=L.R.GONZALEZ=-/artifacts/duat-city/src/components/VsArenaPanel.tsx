import type { CityState } from "../core/types";
import { createVsArenaState } from "../gameModes/vsArenaMode";

export function VsArenaPanel({ state }: { state: CityState }) {
  const arena = createVsArenaState(state);
  return (
    <div className="section">
      <div className="section-title">VS Arena</div>
      {arena.fighters.map(fighter => (
        <div className="stat-row" key={fighter.id}><span className="stat-key">{fighter.faction}</span><span className="stat-val">{fighter.health}</span></div>
      ))}
    </div>
  );
}
