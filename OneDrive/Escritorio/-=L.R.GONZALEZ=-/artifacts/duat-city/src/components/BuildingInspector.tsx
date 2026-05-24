import type { CityState, Building } from "../core/types";
import { BUILDING_DEFS } from "../sim/buildings";
import { GATE_COLORS, rColor, TILE_ICONS } from "../render/palette";

interface BuildingInspectorProps {
  state: CityState;
  buildingId: string;
  onClose: () => void;
}

export function BuildingInspector({ state, buildingId, onClose }: BuildingInspectorProps) {
  const building = state.buildings.find(b => b.id === buildingId);
  if (!building) return null;

  const def = BUILDING_DEFS[building.type];
  const icon = TILE_ICONS[building.type] ?? "";
  const workers = state.agents.filter(a => building.workers.includes(a.id));
  const tile = state.tiles.find(t => t.x === building.x && t.y === building.y);

  return (
    <div className="section">
      <div className="section-title">
        {icon} {building.name}
        <button style={{ float: "right", background: "none", border: "none", color: "#6e7681", cursor: "pointer" }} onClick={onClose}>✕</button>
      </div>
      <div className="stat-row"><span className="stat-key">Type</span><span className="stat-val">{building.type}</span></div>
      <div className="stat-row"><span className="stat-key">Pos</span><span className="stat-val">({building.x},{building.y})</span></div>
      <div className="stat-row"><span className="stat-key">Level</span><span className="stat-val">{building.level}</span></div>
      <div className="stat-row">
        <span className="stat-key">R</span>
        <span className="stat-val" style={{ color: rColor(building.R) }}>{building.R.toFixed(3)}</span>
      </div>
      <div className="stat-row">
        <span className="stat-key">Φ_eff</span>
        <span className="stat-val" style={{ color: rColor(1 - building.Phi_eff) }}>{building.Phi_eff.toFixed(3)}</span>
      </div>
      <div className="stat-row">
        <span className="stat-key">Gate</span>
        <span className="stat-val" style={{ color: GATE_COLORS[building.gate] }}>{building.gate}</span>
      </div>

      {def && (
        <>
          <div style={{ marginTop: 6 }}>
            <span className="stat-key">{def.description}</span>
          </div>
          {Object.keys(def.produces).length > 0 && (
            <div className="stat-row">
              <span className="stat-key">Produces</span>
              <span className="stat-val">{Object.entries(def.produces).map(([k, v]) => `${k}+${v}`).join(", ")}</span>
            </div>
          )}
        </>
      )}

      {tile && (
        <div style={{ marginTop: 4 }}>
          <div className="section-title">FibMob</div>
          <div className="stat-row"><span className="stat-key">μ</span><span className="stat-val">{tile.fibmob.mu}</span></div>
          <div className="stat-row"><span className="stat-key">LOD</span><span className="stat-val">{tile.fibmob.lodFactor.toFixed(2)}</span></div>
          <div className="stat-row"><span className="stat-key">Polarity</span><span className="stat-val">{tile.fibmob.polarity}</span></div>
          <div className="stat-row"><span className="stat-key">Rarity</span><span className="stat-val">{tile.fibmob.rarity.toFixed(4)}</span></div>
        </div>
      )}
    </div>
  );
}
