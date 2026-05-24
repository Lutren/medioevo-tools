import type { CityState } from "../core/types";
import { createRpgModeSummary } from "../gameModes/rpgMode";

export function RpgModePanel({ state }: { state: CityState }) {
  const summary = createRpgModeSummary(state);
  return (
    <div className="section">
      <div className="section-title">RPG Mode</div>
      <div className="stat-row"><span className="stat-key">NPCs</span><span className="stat-val">{summary.npcCount}</span></div>
      <div className="stat-row"><span className="stat-key">Factions</span><span className="stat-val">{summary.factions.length}</span></div>
      <p className="mini-copy">{summary.quests[0] ?? "No quest generated"}</p>
    </div>
  );
}
