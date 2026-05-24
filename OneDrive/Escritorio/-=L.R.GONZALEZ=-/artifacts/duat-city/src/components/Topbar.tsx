import type { CityState } from "../core/types";
import { GATE_COLORS, REGIME_COLORS, rColor } from "../render/palette";

interface TopbarProps {
  state: CityState;
}

export function Topbar({ state }: TopbarProps) {
  const { tick, R, Phi_eff, regime, gate } = state;

  function regimeClass(r: string) {
    if (r === "OPTIMO") return "c-optimo";
    if (r === "FUNCIONAL") return "c-review";
    if (r === "CARGADO") return "c-cargado";
    return "c-block";
  }

  return (
    <div className="topbar">
      <span className="topbar-title">◈ DUAT Agent City</span>
      <span className="topbar-sep">|</span>
      <span className="topbar-stat">
        <span className="topbar-label">TICK</span>
        <span className="topbar-value" style={{ color: "#c9d1d9" }}>{tick}</span>
      </span>
      <span className="topbar-sep">|</span>
      <span className="topbar-stat">
        <span className="topbar-label">R</span>
        <span className="topbar-value" style={{ color: rColor(R) }}>{R.toFixed(3)}</span>
      </span>
      <span className="topbar-stat">
        <span className="topbar-label">Φ_EFF</span>
        <span className="topbar-value" style={{ color: rColor(1 - Phi_eff) }}>{Phi_eff.toFixed(3)}</span>
      </span>
      <span className="topbar-sep">|</span>
      <span className="topbar-stat">
        <span className="topbar-label">REGIME</span>
        <span className={`topbar-value ${regimeClass(regime)}`}>{regime}</span>
      </span>
      <span className="topbar-stat">
        <span className="topbar-label">GATE</span>
        <span className="topbar-value" style={{ color: GATE_COLORS[gate] }}>{gate}</span>
      </span>
      <span className="topbar-sep">|</span>
      <span className="topbar-stat">
        <span className="topbar-label">AGENTS</span>
        <span className="topbar-value" style={{ color: "#7bc8f6" }}>{state.agents.length}</span>
      </span>
      <span className="topbar-stat">
        <span className="topbar-label">BLDGS</span>
        <span className="topbar-value" style={{ color: "#7bc8f6" }}>{state.buildings.length}</span>
      </span>
    </div>
  );
}
