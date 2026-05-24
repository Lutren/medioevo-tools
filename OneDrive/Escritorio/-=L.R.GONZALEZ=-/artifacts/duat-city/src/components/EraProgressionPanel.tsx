import type { EraId } from "../gameModes/gameModeTypes";
import { compileEraConfig, listEras } from "../gameModes/eraProgressionMode";

export function EraProgressionPanel({ era, secretUnlocked, onEra }: { era: EraId; secretUnlocked: boolean; onEra?: (era: EraId) => void }) {
  const config = compileEraConfig(era, secretUnlocked);
  return (
    <div className="section">
      <div className="section-title">Era Progression</div>
      <select value={era} onChange={event => onEra?.(event.target.value as EraId)} className="select-input">
        {listEras(secretUnlocked).map(item => <option key={item.id} value={item.id}>{item.label}</option>)}
      </select>
      <div className="stat-row"><span className="stat-key">Light</span><span className="stat-val">{config.changes.light}</span></div>
      <div className="stat-row"><span className="stat-key">Boundary</span><span className="stat-val">fictional</span></div>
    </div>
  );
}
